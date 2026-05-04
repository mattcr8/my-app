<!DOCTYPE html>
<html>
<head>
    <title>AI Betting Pro</title>
    <style>
        body {
            background: #0d0d0d;
            color: white;
            font-family: Arial;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        .card {
            border-radius: 15px;
            padding: 20px;
            margin: 20px auto;
            width: 90%;
            max-width: 500px;
            background: #1a1a1a;
        }

        .green {
            border: 2px solid #00ff00;
        }

        .red {
            border: 2px solid red;
        }

        .title {
            font-size: 20px;
            font-weight: bold;
        }

        .highlight {
            color: #00ffff;
        }

        .goal {
            color: orange;
        }

        .decision {
            font-size: 22px;
            font-weight: bold;
            margin-top: 10px;
        }

        .confidence {
            color: lightgray;
        }
    </style>
</head>

<body>

<h1>🔥 AI BETTING PRO</h1>

{% for m in matches %}
<div class="card {{ 'green' if m.decision == 'NEXT GOAL' else 'red' }}">
    
    <div class="title">{{ m.home }} vs {{ m.away }}</div>

    <p>Score: {{ m.score }}</p>
    <p>Minute: {{ m.minute }}</p>

    <p class="highlight">Shots: {{ m.shots }}</p>
    <p class="highlight">xG: {{ m.xg }}</p>

    <p class="goal">Goal Probability: {{ m.prob_goal }}%</p>

    <div class="decision">
        {% if m.decision == "NEXT GOAL" %}
            🔥 NEXT GOAL
        {% else %}
            ❌ NO BET
        {% endif %}
    </div>

    <p class="confidence">Confidence: {{ m.confidence }}%</p>
    <p>🧠 {{ m.reason }}</p>

</div>
{% endfor %}

</body>
</html>