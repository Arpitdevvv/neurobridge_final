from flask import Flask, render_template, jsonify, request
import subprocess
import os
import sys

from agent.cognition_agent import analyze_student

app = Flask(__name__)

# ---------------- HOME ---------------- #

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# ---------------- COGNITION ---------------- #

@app.route('/run/cognition')
def run_cognition():
    return render_template('cognition.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()

        problem = data.get("problem", "")
        confidence = int(data.get("confidence", 5))

        result = analyze_student(problem, confidence)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- OTHER AGENTS ---------------- #

@app.route('/run/emotion')
def run_emotion():
    return jsonify({
        "status": "success",
        "message": "Emotion Agent launched",
        "url": "http://127.0.0.1:5001"
    })


@app.route('/run/planner')
def run_planner():
    return launch_agent('agent/plan.pyw')


@app.route('/run/rewritter')
def run_rewritter():
    return launch_agent('agent/rewritter.py')


@app.route('/run/tutor')
def run_tutor():
    return launch_agent('agent/tutor.py')


@app.route('/run/progress')
def run_progress():
    return launch_agent('agent/progress.py')


# ---------------- AGENT LAUNCHER ---------------- #

def launch_agent(script_path):
    abs_path = os.path.join(os.path.dirname(__file__), script_path)

    print("Launching:", abs_path)
    print("Python:", sys.executable)

    if not os.path.exists(abs_path):
        return jsonify({"error": f"Not found: {abs_path}"}), 404

    try:
        subprocess.Popen(
            [sys.executable, abs_path],
            cwd=os.path.dirname(abs_path)
        )

        return jsonify({
            "status": "success",
            "message": f"Launching {os.path.basename(script_path)}"
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)