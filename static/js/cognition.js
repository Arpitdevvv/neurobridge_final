const problem = document.getElementById("problem");

problem.addEventListener("change", updateQuestion);

updateQuestion();

function updateQuestion() {

    const value = problem.value;

    const title = document.getElementById("dynamicTitle");
    const question = document.getElementById("dynamicQuestion");

    if (value === "I don't understand the concept.") {

        title.innerHTML = "🧠 Understanding Level";

        question.innerHTML =
        `How well do you currently understand this topic?<br><br>
        <b>1</b> = Completely confused<br>
        <b>5</b> = Understand some parts<br>
        <b>10</b> = Understand everything`;

    }

    else if (value === "I understand the concept but forget it quickly.") {

        title.innerHTML = "🧠 Memory Retention";

        question.innerHTML =
        `After one day, how much do you remember?<br><br>
        <b>1</b> = Almost nothing<br>
        <b>5</b> = Around half<br>
        <b>10</b> = Almost everything`;

    }

    else if (value === "I know the concept but cannot solve questions.") {

        title.innerHTML = "🧠 Application Ability";

        question.innerHTML =
        `How well can you solve problems?<br><br>
        <b>1</b> = Cannot solve<br>
        <b>5</b> = Can solve easy questions<br>
        <b>10</b> = Can solve almost everything`;

    }

    else {

        title.innerHTML = "🧠 Focus Level";

        question.innerHTML =
        `How focused are you while studying?<br><br>
        <b>1</b> = Constantly distracted<br>
        <b>5</b> = Sometimes distracted<br>
        <b>10</b> = Fully focused`;

    }

}

async function analyzeStudent() {

    console.log("Analyze button clicked");

    const output = document.getElementById("output");

    output.innerHTML = "Analyzing...";

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                problem: document.getElementById("problem").value,
                confidence: document.getElementById("confidence").value

            })

        });

        console.log("Response received");

        const data = await response.json();

        console.log(data);

        if (data.error) {

            output.innerHTML = "<pre>" + data.error + "</pre>";
            return;

        }

        output.innerHTML = `
<b>Problem Type:</b> ${data.problem_type}<br><br>

<b>Confidence Level:</b> ${data.confidence_level}<br><br>

<b>Cognitive Load:</b> ${data.cognitive_load}<br><br>

<b>Emotion:</b> ${data.emotion}<br><br>

<b>Learning Style:</b> ${data.learning_style}<br><br>

<b>Recommended Strategy:</b> ${data.recommended_strategy}<br><br>

<b>Next Step:</b> ${data.next_step}
`;

    }

    catch (err) {

        console.error(err);

        output.innerHTML =
        "<pre>" + err + "</pre>";

    }

}