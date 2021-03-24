// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import { SidebarProvider } from "./SidebarProvider";

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
		vscode.commands.registerCommand('vstool.helloWorld', () => {
			vscode.window.showInformationMessage('Hello World!');
		})
	);

	context.subscriptions.push(
		vscode.commands.registerCommand("vstodo.refresh", async () => {
		  // HelloWorldPanel.kill();
		  // HelloWorldPanel.createOrShow(context.extensionUri);
		  await vscode.commands.executeCommand("workbench.action.closeSidebar");
		  await vscode.commands.executeCommand(
			"workbench.view.extension.vstool-sidebar-view"
		  );
		  // setTimeout(() => {
		  //   vscode.commands.executeCommand(
		  //     "workbench.action.webview.openDeveloperTools"
		  //   );
		  // }, 500);
		})
	  );
}

// this method is called when your extension is deactivated
export function deactivate() {}
