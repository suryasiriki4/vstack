# team09_tool

## ABOUT :
A software tool which improves the human computer interaction by solving developers routine problem of swtiching to web browser for accessing stackoverflow to search for a query or question and also give the summary of error along with a short summarized solution from stackoverflow after compilation.

## this vs code extension consists of mainly two features :
* A side panel for searching any query or issue in stackoverflow and getting the most relevant results.
* Generating more readable errors, by summarizing the error message and shortly summarized solution from stack overflow.

## Images of Side Panel for accessing Stack Oveflow
### Release 1:
![Alt text](./images/release_1.gif?raw=true "Side Panel in vscode extension")

### Release 2:
![Alt text](./images/release_21.gif?raw=true "Giving readable, summarized error messages")

![Alt text](./images/release_22.gif?raw=true "stackoverflow solutions for the errors")

### Setup script :
```console
# clone the repository your development environment
git clone https://github.com/suryasiriki4/team09_tool.git

# cd into the project directory
cd team09_tool/

# install packages required to run the tool
* pipenv install 
* pipenv shell   /* in server folder to install all the packages required in server*/

* npm install /* in client folder to install all packages required in client*/
``` 

### Run script :
* python3 server.py  /* in server folder */
* npm run watch      /* in client folder */
then press f5 to start dev env in visual studio.

