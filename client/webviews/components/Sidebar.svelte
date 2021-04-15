<script>

    let arrayOfQuestions;

    async function fetchFromServer() {

        // declarations

        const question1 = document.getElementById("question1");
        const question2 = document.getElementById("question2");
        const question3 = document.getElementById("question3");
        const question4 = document.getElementById("question4");

        const loaders = document.getElementsByClassName("loader");
        var loader = null;
        if (loaders.length > 0 ) {
            loader = loaders[0];
        }

        var viewButtons = document.getElementsByClassName("viewButton");

        const fullQuestion = document.getElementById("fullQuestion");
        const fullAnswer = document.getElementById("fullAnswer");

        const lines = document.getElementsByClassName("dotted");

        const questionTitles = document.getElementsByTagName("h3");


        // cleaning the panel for the new results

        question1.innerText = '';
        question2.innerText = '';
        question3.innerText = '';
        question4.innerText = '';

        for (var i = 0; i < viewButtons.length; ++i) {
            viewButtons[i].style.visibility = "hidden"; 
        }

        for (var i = 0; i < lines.length; ++i) {
            lines[i].style.visibility = "hidden";
        }
        
        questionTitles[0].style.visibility = "hidden";
        questionTitles[1].style.visibility = "hidden";

    

        fullQuestion.innerText = '';
        fullAnswer.innerText = '';

        fullAnswer.style.visibility = "hidden";


        console.log("button is clicked");

        const searchJson = JSON.stringify(
        {
        "search" : document.getElementsByClassName('searchQuery')[0].value
        });

        if (loader) {
            loader.style.visibility = "visible";
        }

        const response = await fetch('http://0.0.0.0:5000/receiver', {
            method: 'POST',
            body: searchJson,
            headers: {
                'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(res => res.json());

        console.log(response);

        if (loader) {
            loader.remove();
        }

        var parsedJSON = response;

        arrayOfQuestions = parsedJSON.Questions;

        console.log(arrayOfQuestions);

        question1.innerText = arrayOfQuestions[0].Title + "...";
        question2.innerText = arrayOfQuestions[1].Title + "...";
        question3.innerText = arrayOfQuestions[2].Title + "...";
        question4.innerText = arrayOfQuestions[3].Title + "...";

        for (var i = 0; i < viewButtons.length; ++i) {
            viewButtons[i].style.visibility = "visible"; 
        }

        for (var i = 0; i < lines.length; ++i) {
            lines[i].style.visibility = "visible";
        }


        document.getElementsByClassName('searchQuery')[0].value = '';

        // document.getElementById("Result").style.display = "box";
        // document.getElementById("Options").style.dispaly = "box";
    }

    //printing full question and answer at the end

    function printFullQuestion(num_of_question) {
        const fullQuestion = document.getElementById("fullQuestion");
        const fullAnswer = document.getElementById("fullAnswer");

        const questionTitles = document.getElementsByTagName("h3");
        questionTitles[0].style.visibility = "visible";
        questionTitles[1].style.visibility = "visible";

        fullAnswer.style.visibility = "visible";

        fullQuestion.innerText = arrayOfQuestions[num_of_question-1].Title;
        fullAnswer.innerText = arrayOfQuestions[num_of_question-1].Answer;
    }
</script>
<style>
  #Options{
      display: none;
  }
  #Result{
    display: none;
  }

  hr.dotted {
    border-top: 0.5px dotted var(--vscode-foreground);
  }

  .viewButton {
    border-radius: 4px;
    background-color: var(--vscode-button-background);
    border: none;
    color: #FFFFFF;
    text-align: center;
    font-size: 12px;
    padding: 5px;
    width: 120px;
    transition: all 0.5s;
    cursor: pointer;
    margin: 0.1px;
    }

    .viewButton span {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }

    .viewButton span:after {
    content: '\00bb';
    position: absolute;
    opacity: 0;
    top: 0;
    right: -20px;
    transition: 0.5s;
    }

    .viewButton:hover span {
    padding-right: 25px;
    }

    .viewButton:hover span:after {
    opacity: 1;
    right: 0;
    }

    .loader {
    border: 5px solid var(--vscode-foreground); /* Light grey */
    border-top: 5px solid var(--vscode-button-background); /* Blue */
    border-bottom: 5px solid var(--vscode-button-background); /* Blue */
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 2s linear infinite;
    }

    .loader-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
    }

    div#fullAnswer {
        background-color: var(--vscode-foreground);
        color: var(--vscode-editor-background);
        height: 200px;
        width: 300px;
        overflow-y: scroll;
    }
</style>
<input class="searchQuery" id="myInput"/>
<div for="topQ" id = "Result">Top Search Results:</div>

<select id="Options">
    
    <option>Option1</option>

    
</select>
<button id="myBtn" class="btn" on:click ={fetchFromServer}>
    Search
</button>

<div class="loader-container">
    <div class="loader" style="visibility:hidden"></div>
</div>


<p id="question1"></p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(1)}><span>Question 1</span></button>
<hr class="dotted" style="visibility:hidden">
<p id="question2"></p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(2)}><span>Question 2</span></button>
<hr class="dotted" style="visibility:hidden">
<p id="question3"></p>
<button class="viewButton"  style="visibility:hidden" on:click={() => printFullQuestion(3)}><span>Question 3</span></button>
<hr class="dotted" style="visibility:hidden">
<p id="question4"></p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(4)}><span>Question 4</span></button>
<hr class="dotted" style="visibility:hidden">
<br>
<h3 style="visibility:hidden">QUESTION:</h3>
<p id="fullQuestion"></p>
<br>
<h3 style="visibility:hidden">ANSWER:</h3>
<div style="visibility:hidden" id="fullAnswer">
</div>

