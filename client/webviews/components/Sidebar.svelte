<script>


    async function fetchFromServer() {


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

        var arrayOfQuestions = parsedJSON.Questions;

        console.log(arrayOfQuestions);

        const question1 = document.getElementById("question1");
        const question2 = document.getElementById("question2");
        const question3 = document.getElementById("question3");
        const question4 = document.getElementById("question4");


        question1.innerText = arrayOfQuestions[0];
        question2.innerText = arrayOfQuestions[1];
        question3.innerText = arrayOfQuestions[2];
        question4.innerText = arrayOfQuestions[3];


        // document.getElementById("Result").style.display = "box";
        // document.getElementById("Options").style.dispaly = "box";
    }
</script>
<style>
  #Options{
      display: none;
  }
  #Result{
    display: none;
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
<p id="question2"></p>
<p id="question3"></p>
<p id="question4"></p>
