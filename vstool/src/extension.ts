// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { SidebarProvider } from "./SidebarProvider";
import { WindowPanel } from "./WindowPanel";

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	const sidebarProvider = new SidebarProvider(context.extensionUri);
	context.subscriptions.push(
	  vscode.window.registerWebviewViewProvider(
		"vstool-sidebar",
		sidebarProvider
	  )
	);

	context.subscriptions.push(
		vscode.commands.registerCommand("vstool.welcomeMessage", async () => {
			const answ = await vscode.window.showInformationMessage("How was your Day?","Good","Bad");
			if(answ == "bad"){
				vscode.window.showInformationMessage("Sorry to hear that");
			}
			else{
				vscode.window.showInformationMessage("Happy Coding!!");
			}
		})
	);

	context.subscriptions.push(
		vscode.commands.registerCommand("vstool.addWindow",() => {
			WindowPanel.createOrShow(context.extensionUri);

		})
	);

	// context.subscriptions.push(
	// 	vscode.commands.registerCommand("vstodo.refresh", async () => {
	// 	  // HelloWorldPanel.kill();
	// 	  // HelloWorldPanel.createOrShow(context.extensionUri);
	// 	  await vscode.commands.executeCommand("workbench.action.closeSidebar");
	// 	  await vscode.commands.executeCommand(
	// 		"workbench.view.extension.vstool-sidebar-view"
	// 	  );
	// 	  // setTimeout(() => {
	// 	  //   vscode.commands.executeCommand(
	// 	  //     "workbench.action.webview.openDeveloperTools"
	// 	  //   );
	// 	  // }, 500);
	// 	})
	//   );
}

// this method is called when your extension is deactivated
export function deactivate() {}
