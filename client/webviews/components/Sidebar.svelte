<!-- 
    This module contains handles all the html, css and js
    of the side panel:
 -->

<script>

    // final array of results from the backend
    let arrayOfQuestions;

    async function fetchFromServer() {

        // declarations
        const question1 = document.getElementById("question1");
        const question2 = document.getElementById("question2");
        const question3 = document.getElementById("question3");

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

        // initally hiding the buttons and lines in the panel
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

        const searchJson = JSON.stringify(
        {
        "search" : document.getElementsByClassName('searchQuery')[0].value
        });
        
        // making the loader component visible
        if (loader) {
            loader.style.visibility = "visible";
        }

        const response = await fetch('http://0.0.0.0:5000/receiver', {
            method: 'POST',
            body: searchJson,
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(res => res.json());

        console.log(response);

        // removing the loader component when the results are fetched
        if (loader) {
            loader.remove();
        }

        // getting the array of results from the response received from backend
        var parsedJSON = response;
        arrayOfQuestions = parsedJSON.Questions;

        // making sure that the number of results received are 3 by adding dummy results
        while (arrayOfQuestions.length < 3) {
            arrayOfQuestions.push({
                Answer: "NULL",
                Answers: 0,
                Title: "NULL",
                TitleTrunc: "NULL",
                URL: "didn't get",
                index: arrayOfQuestions.length()
            })
        }

        // adding the titles of questions from stackoverflow to text components
        question1.innerText = arrayOfQuestions[0].TitleTrunc + "...";
        question2.innerText = arrayOfQuestions[1].TitleTrunc + "...";
        question3.innerText = arrayOfQuestions[2].TitleTrunc + "...";

        // making the buttons and lines visible after results are fetched
        for (var i = 0; i < viewButtons.length; ++i) {
            viewButtons[i].style.visibility = "visible"; 
        }
        for (var i = 0; i < lines.length; ++i) {
            lines[i].style.visibility = "visible";
        }

        // removing the text in the search box.
        document.getElementsByClassName('searchQuery')[0].value = '';
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
  /* styling the line dividers */
  hr.dotted {
    border-top: 0.5px dotted var(--vscode-foreground);
  }

   /* styling the view quetion buttons */
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

    /* styling the loader */
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

    /* styling the full answer to be displayed */
    div#fullAnswer {
        background-color: var(--vscode-foreground);
        color: var(--vscode-editor-background);
        height: 200px;
        width: 300px;
        overflow-y: scroll;
    }
</style>

<!-- search box and search button -->
<input class="searchQuery" id="myInput"/>
<button id="myBtn" class="btn" on:click ={fetchFromServer}>
    Search
</button>

<!-- loader component -->
<div class="loader-container">
    <div class="loader" style="visibility:hidden"></div>
</div>

<!-- 3 questions to be displayed in the side panel -->
<p id="question1"></p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(1)}><span>Question 1</span></button>
<hr class="dotted" style="visibility:hidden">
<p id="question2"></p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(2)}><span>Question 2</span></button>
<hr class="dotted" style="visibility:hidden">
<p id="question3"></p>
<button class="viewButton" style="visibility:hidden"  on:click={() => printFullQuestion(3)}><span>Question 3</span></button>
<hr class="dotted" style="visibility:hidden">

<br>

<!-- diplaying entire question and answer when the button is clicked -->
<h3 style="visibility:hidden">QUESTION:</h3>
<p id="fullQuestion"></p>
<br>
<h3 style="visibility:hidden">ANSWER:</h3>
<div style="visibility:hidden" id="fullAnswer">
</div>