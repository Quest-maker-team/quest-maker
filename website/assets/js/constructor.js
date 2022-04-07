import { newInstance } from "@jsplumb/browser-ui";
import {Endpoint} from "@jsplumb/core";
import { FlowchartConnector } from "@jsplumb/connector-flowchart";
import { Render } from "./render"
import { TestJSON } from "./testJSON";

let containerElement = document.getElementById("container");

let instance = newInstance({
    container: containerElement,
});

/*let startBlock = document.getElementById("start");
let finishBlock = document.getElementById("finish");*/

let sourceEndpoint = {
    endpoint: { type: "Dot", options: { radius: 5 } },
    //paintStyle: { fill: "red" },
    //connectorStyle: { stroke: 'red', strokeWidth: 3 },
    connector: { type: "Flowchart", options: { cornerRadius: 2 } },
    source: true,
    //anchor: [ 0.5, 1, 0, 1 ],
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

/*let startEndpoint = instance.addEndpoint(startBlock, { anchor:[ 0.5, 1, 0, 1 ] }, sourceEndpoint);
let finishEndpoint = instance.addEndpoint(finishBlock, { anchor:[ 0.5, 0, 0, -1 ]}, targetEndpoint);*/

/*instance.connect({
    source: startEndpoint,
    target: finishEndpoint,
    connector:{
        type:"Flowchart",
        options:{
            cornerRadius: 2
        }
    },
    detachable: true,
});*/

Render(TestJSON, instance, sourceEndpoint, targetEndpoint);
//instance.addEndpoint(containerElement, sourceEndpoint);