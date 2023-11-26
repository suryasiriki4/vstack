# VStack

## ABOUT :
Did you know that an average developer spends 12.5% of his time on "Stack overflow"?

Switching to browser can be a dangerous for developer's productivity.

VStack gives answers to your queries in your IDE. Vstack also gives "Stack overflow" results for errors in your program.

With VStack you don't even have to switch a tab to access "stack overflow".

[VStack Demo Video](https://youtu.be/-YNVzYT7Az0)

## this vs code extension consists of mainly two features :
* A side panel for searching any query or issue in stackoverflow and getting the most relevant results.
* Generating more readable errors, by summarizing the error message and shortly summarized solution from stack overflow.

## Images of Side Panel for accessing Stack Oveflow
### Release 1:
![Alt text](/images/release_1.gif "Side Panel in vscode extension")

### Release 2:
![Alt text](/images/release_21.gif "Giving readable, summarized error messages")

![Alt text](/images/release_22.gif "stackoverflow solutions for the errors")

### Setup script :
```console
# clone the repository your development environment
git clone https://github.com/suryasiriki4/team09_tool.git

# cd into the project directory
cd team09_tool/

# install packages required to run the tool
* cd server
* pipenv install /* in server directory to install all the packages required in server*/
* cd client
* npm install /* in client directory to install all packages required in client*/
``` 

### Run script :
```console
* cd server
* python3 server.py  /* in server folder */
* cd client
* npm run watch      /* in client folder */
then press f5 to start dev env in visual studio.
``` 
```console
Feature 2:
* cd server
* pipenv install torch
* python3 resolver.py ./errror_resolver/tests/test_4.py   /* in server directory */
``` 
