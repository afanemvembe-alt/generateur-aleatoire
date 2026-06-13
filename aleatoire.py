import os
import secrets
import string
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Design de la page Web (HTML/Tailwind CSS) directement intégré
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Générateur de Mot de Passe Sécurisé</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 font-sans min-h-screen flex items-center justify-center p-4">
    <div class="bg-white p-6 sm:p-8 rounded-2xl shadow-md border border-slate-100 max-w-md w-full">
        <h1 class="text-2xl font-extrabold text-slate-900 text-center mb-2">Générateur de Mot de Passe</h1>
        <p class="text-sm text-slate-500 text-center mb-6">Créez un mot de passe fort et personnalisé</p>
        
        <div class="space-y-4">
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1">Fruit préféré</label>
                <input type="text" id="fruit" placeholder="Ex: Tomate" class="w-full border border-slate-200 rounded-xl p-2.5 outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1">Animal préféré</label>
                <input type="text" id="animal" placeholder="Ex: Chien" class="w-full border border-slate-200 rounded-xl p-2.5 outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1">Date de naissance</label>
                <input type="text" id="date" placeholder="Ex: 1995" class="w-full border border-slate-200 rounded-xl p-2.5 outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            <div>
                <label class="block text-sm font-semibold text-slate-700 mb-1">Longueur totale</label>
                <input type="number" id="length" value="12" min="1" class="w-full border border-slate-200 rounded-xl p-2.5 outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            
            <button onclick="generatePassword()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl transition shadow-sm mt-2">
                Générer le mot de passe
            </button>
            
            <div class="pt-4 border-t border-slate-100 flex gap-2">
                <input type="text" id="result" readonly placeholder="Votre mot de passe apparaîtra ici" 
                       class="w-full border border-slate-200 rounded-xl p-2.5 bg-slate-50 text-center font-mono font-bold text-slate-700 outline-none">
                <button onclick="copyPassword()" class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 rounded-xl transition">
                    Copier
                </button>
            </div>
        </div>
    </div>

    <script>
        async function generatePassword() {
            const data = {
                fruit: document.getElementById('fruit').value,
                animal: document.getElementById('animal').value,
                date: document.getElementById('date').value,
                length: parseInt(document.getElementById('length').value) || 12
            };

            const response = await fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            if (result.error) {
                alert(result.error);
            } else {
                document.getElementById('result').value = result.password;
            }
        }

        function copyPassword() {
            const psw = document.getElementById('result').value;
            if (!psw) return alert("Rien à copier !");
            navigator.clipboard.writeText(psw);
            alert("Mot de passe copié !");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    fruit = data.get('fruit', '').strip()
    animal = data.get('animal', '').strip()
    date = data.get('date', '').strip()
    
    try:
        length = int(data.get('length', 12))
        if length <= 0:
            return jsonify({"error": "La longueur doit être supérieure à 0."})
    except ValueError:
        return jsonify({"error": "Longueur invalide."})

    criteria = [x for x in [fruit, animal, date] if x]
    base = "".join(criteria)
    
    if not base:
        return jsonify({"error": "Veuillez remplir au moins un critère."})
        
    if length < len(base):
        return jsonify({"error": f"Longueur trop courte. Minimum requis : {len(base)} caractères."})

    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    remaining_length = length - len(base)
    random_part = ''.join(secrets.choice(characters) for _ in range(remaining_length))
    
    password_list = list(base + random_part)
    secrets.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    
    return jsonify({"password": password})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
