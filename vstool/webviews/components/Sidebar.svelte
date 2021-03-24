
<script>
    import * as vscode from 'vscode';
    import { WindowPanel } from ".../src/WindowPanel.ts";
    function callSearch(){
        context.subscriptions.push(
		vscode.commands.registerCommand("vstool.addWindow",() => {
			WindowPanel.createOrShow(context.extensionUri);

		})
	);
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