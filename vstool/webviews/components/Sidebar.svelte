<script>
    function callSearch(){
        document.getElementById(Result).style.display = "box";
        document.getElementById(Options).style.dispaly = "box";
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
<input/>
<div for="topQ" id = "Result">Top Search Results:</div>
<select id="Options">
    
    <option>Option1ffffffffffffffffffffffffffffffff</option>
    <option>Option2</option>
    <option>Option3</option>
    
</select>
<button on:click ={callSearch}>
    Search
</button>