<script>

    let arrayOfQuestions;

    async function fetchFromServer() {

        // declarations

        const question1 = document.getElementById("question1");
        const question2 = document.getElementById("question2");
        const question3 = document.getElementById("question3");
        const question4 = document.getElementById("question4");

        var viewButtons = document.getElementsByClassName("viewButton");

        const fullQuestion = document.getElementById("fullQuestion");
        const fullAnswer = document.getElementById("fullAnswer");

        // cleaning the panel for the new results

        question1.innerText = 'Loading';
        question2.innerText = '';
        question3.innerText = '';
        question4.innerText = '';

        for (var i = 0; i < viewButtons.length; ++i) {
            viewButtons[i].style.visibility = "hidden"; 
        }

        fullQuestion.innerText = '';
        fullAnswer.innerText = '';


        console.log("button is clicked");

        const searchJson = JSON.stringify(
        {
        "search" : document.getElementsByClassName('searchQuery')[0].value
        });

        const response = await fetch('http://0.0.0.0:5000/receiver', {
            method: 'POST',
            body: searchJson,
            headers: {
                'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(res => res.json());

        var parsedJSON = response;

        arrayOfQuestions = parsedJSON.Questions;

        console.log(arrayOfQuestions);

        question1.innerText = arrayOfQuestions[0][0].substr(0, 100);
        question2.innerText = arrayOfQuestions[1][0].substr(0, 100);
        question3.innerText = arrayOfQuestions[2][0].substr(0, 100);
        question4.innerText = arrayOfQuestions[3][0].substr(0, 100);

        for (var i = 0; i < viewButtons.length; ++i) {
            viewButtons[i].style.visibility = "visible"; 
        }


        document.getElementsByClassName('searchQuery')[0].value = '';

        // document.getElementById("Result").style.display = "box";
        // document.getElementById("Options").style.dispaly = "box";
    }

    //printing full question and answer at the end

    function printFullQuestion(num_of_question) {
        const fullQuestion = document.getElementById("fullQuestion");
        const fullAnswer = document.getElementById("fullAnswer");

        fullQuestion.innerText = arrayOfQuestions[num_of_question-1][0];
        fullAnswer.innerText = arrayOfQuestions[num_of_question-1][2];
    }
</script>
<style>
  #Options{
      display: none;
  }
  #Result{
    display: none;
  }

  hr.dashed {
    border-top: 1px dashed var(--vscode-foreground);
  }

  hr.dotted {
    border-top: 1px dotted var(--vscode-foreground);
  }
</style>
<input class="searchQuery"/>
<div for="topQ" id = "Result">Top Search Results:</div>

<select id="Options">
    
    <option>Option1ffffffffffffffffffffffffffffffff</option>

    
</select>
<button on:click ={fetchFromServer}>
    Search
</button>

<p id="question1">Loading...</p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(1)}>question 1</button>
<hr class="dashed">
<p id="question2"></p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(2)}>question 2</button>
<hr class="dashed">
<p id="question3"></p>
<button class="viewButton"  style="visibility:hidden" on:click={() => printFullQuestion(3)}>question 3</button>
<hr class="dashed">
<p id="question4"></p>
<button class="viewButton" style="visibility:hidden" on:click={() => printFullQuestion(4)}>question 4</button>
<hr class="dashed">
<br>
<br>
<h3>QUESTION:</h3>
<p id="fullQuestion"></p>
<hr class="dotted">
<br>
<h3>ANSWER:</h3>
<p id="fullAnswer"></p>
