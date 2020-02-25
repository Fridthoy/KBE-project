# Knowledge-based_engineering_project

We were tasked with making a automated system for chair-manufacturing based on KBE(Knowledge-based engineering). The system would provide
a interface to be accessed on the web. Both customers and engnieers could input desired measurements and productionlimits respectivly.
This would then be send to the server that would update a Knowledge Fusion template and update it in Siemens NX. The goal of the project
was to automate the whole process, and incorporates a number of different systems. 

![alt text](https://github.com/anderf2706/Knowledge-based_engineering_project/blob/master/Merknad%202020-02-25%20131626.png)


## Getting Started

To get started you need to change path variables in hte DFA-server.py file, to access the right folder for dfa-templates. You also 
need to have a fuseki-server running with a correct OWL-file for queries. 

### Prerequisites

-Python 3.7 \
-Fuseki-server\
-Siemenes NX 

## Architecture

![alt text](https://github.com/anderf2706/Knowledge-based_engineering_project/blob/master/Merknad%202020-02-25%20131626.png)

## Running the system

To run the system start running the fuseki-server, then start DFA-server and manufReqServer. Go to the local-url provided in the server-code.
Then enter the max-min requierments and the customer-input. The system will tell you your choices, and if the product can be made with regards
to the constraints set. the DFA-file will update and the new chair will be displayed in NX.

**GUI:**
![GUI](https://github.com/anderf2706/Knowledge-based_engineering_project/blob/master/Merknad%202020-02-25%20131735.png)


## Deployment

To make the system fully operational, one would have to deploy it online using an existing server, or cloud-based through GCloud app engine
or similar solutions. 

## Authors

* **Marianne Pettersen**
* **Fridtjof Høyer**
* **Anders Fredriksen**

## Acknowledgments

This code was developed during 5 four hour sessions.
Inspiration and project-idea goes to Andrei Lobov.  
