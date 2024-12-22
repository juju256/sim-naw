from flask import Flask, render_template, request, jsonify
from simucombats import Joueur, combat  # Assurez-vous d'importer vos classes et fonctions existantes

app = Flask(__name__)

# Joueurs globaux
joueur1 = Joueur("Joueur 1")
joueur2 = Joueur("Joueur 2")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/configurer_joueurs", methods=["POST"])
def configurer_joueurs():
    try:
        joueur1_data = request.form["joueur1"]
        joueur2_data = request.form["joueur2"]
        joueur1.importer_unites_depuis_texte(joueur1_data)
        joueur2.importer_unites_depuis_texte(joueur2_data)
        return jsonify({"message": "Joueurs configurés avec succès !", "status": "success"})
    except Exception as e:
        return jsonify({"message": f"Erreur de configuration : {e}", "status": "error"})

@app.route("/configurer_bonus", methods=["POST"])
def configurer_bonus():
    try:
        joueur1.mandibule = int(request.form.get("joueur1_mandibule", 0))
        joueur1.carapace = int(request.form.get("joueur1_carapace", 0))
        joueur1.dome = int(request.form.get("joueur1_dome", 0))
        joueur1.loge = int(request.form.get("joueur1_loge", 0))

        joueur2.mandibule = int(request.form.get("joueur2_mandibule", 0))
        joueur2.carapace = int(request.form.get("joueur2_carapace", 0))
        joueur2.dome = int(request.form.get("joueur2_dome", 0))
        joueur2.loge = int(request.form.get("joueur2_loge", 0))

        return jsonify({"message": "Bonus configurés avec succès !", "status": "success"})
    except Exception as e:
        return jsonify({"message": f"Erreur de configuration des bonus : {e}", "status": "error"})

@app.route("/lancer_combat", methods=["POST"])
def lancer_combat():
    try:
        environment = request.form["environment"]
        rapport = combat(joueur1, joueur2, environment)
        return jsonify({"rapport": rapport, "status": "success"})
    except Exception as e:
        return jsonify({"message": f"Erreur lors du lancement du combat : {e}", "status": "error"})

if __name__ == "__main__":
    app.run(debug=True)
