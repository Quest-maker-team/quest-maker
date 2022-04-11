import { newInstance } from "@jsplumb/browser-ui";
import { FlowchartConnector } from "@jsplumb/connector-flowchart";
//import { Render } from "./render"
import { Render } from "./render";
import {TestJSON} from "./testJSON";
let staticQuest;

export class Quest{
    constructor(test) {
       this.data = test;
       staticQuest = this;
       console.log(this.data.description);
       this.showQuest(test);
    }
    static createQuest(){
        const id = 2;
        Quest.loadQuest(id);
    }
    static getQuest(){
        return staticQuest;
    }
     static loadQuest(id){
        let url = '/api/db/quest/'+id.toString();
        console.log(url);
        
        let xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                console.log('responseText:' + xmlhttp.responseText);
                let data;
                try {
                     data = JSON.parse(xmlhttp.responseText);
                     console.log(data);
                } catch(err) {
                    console.log(err.message + " in " + xmlhttp.responseText);
                    return;
                }
                console.log(data); 
                new Quest(data);
            }
        };
     
        xmlhttp.open("GET", url, true);
        xmlhttp.send()
    }
showQuest(){
    console.log(this);
    let quest = Quest.getQuest();
    let containerElement = document.getElementById("container");

let instance = newInstance({
    container: containerElement,
});

let sourceEndpoint = {
    endpoint: { type: "Dot", options: { radius: 5 } },
    connector: { type: "Flowchart", options: { cornerRadius: 2 } },
    source: true,
};

let targetEndpoint = {
    endpoint: { type: "Rectangle" },
    //paintStyle: { fill: "green" },
    maxConnections: -1,
    source: false,
    target: true,
    connectionsDetachable: true,
    anchor: [ 0.5, 0, 0, -1 ],
};
    Render.Render(quest, instance, sourceEndpoint, targetEndpoint);
    
  }

}