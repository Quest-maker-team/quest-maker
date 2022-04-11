import {newInstance} from "@jsplumb/browser-ui";
//import { Render } from "./render"
import {Render} from "./render";

export class Quest{
    constructor(data) {
       this.data = data;
    }

    static makeLoadRequest(url){
        return new Promise(function (resolve, reject) {
            let xmlhttp = new XMLHttpRequest();

            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    if (xmlhttp.status === 200) {
                        resolve(xmlhttp.responseText);
                    } else {
                        reject(xmlhttp.status);
                    }
                }
            };
            xmlhttp.open("GET", url, true);
            xmlhttp.send();
        });
    }

    static loadQuest(id){
        let url = '/api/db/quest/' + id.toString();

        return new Promise((resolve, reject) => {
            resolve(this.makeLoadRequest(url).then(data => {
                console.log("success");
                return new Quest(JSON.parse(data));
            }));
        });
    }

    showQuest(){
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
            maxConnections: -1,
            source: false,
            target: true,
            connectionsDetachable: true,
            anchor: [ 0.5, 0, 0, -1 ],
        };

        Render.render(this, instance, sourceEndpoint, targetEndpoint);
    }
}