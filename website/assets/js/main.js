import { newInstance } from "@jsplumb/browser-ui";
import { FlowchartConnector } from "@jsplumb/connector-flowchart";

let containerElement = document.getElementById("container");

let instance = newInstance({
    container:containerElement
});

// parent block
let parent1 = document.getElementById("parent1");
let parent2 = document.getElementById("parent2");
let parent3 = document.getElementById("parent3");
let parent4 = document.getElementById("parent4");
//child blocks
let child1 = document.getElementById("child1");
let child2 = document.getElementById("child2");

let exampleDropOptions1 = {
    tolerance: "touch",
    hoverClass: "dropHover",
    activeClass: "dragActive"
};

let exampleEndpoint1 = {
    endpoint: { type: "Dot", options: { radius: 5 } },
    paintStyle: { fill: "red" },
    connectorStyle: { stroke: 'red', strokeWidth: 3 },
    connector: { type: "Flowchart", options: { cornerRadius: 2 } },
    source: true,
};

instance.addEndpoint(parent1, { anchor:[ 0.5, 1, 0, 1 ] }, exampleEndpoint1);
instance.addEndpoint(parent2, { anchor:[ 0.5, 1, 0, 1 ] }, exampleEndpoint1);
instance.addEndpoint(parent3, { anchor:[ 0.5, 1, 0, 1 ] }, exampleEndpoint1);
instance.addEndpoint(parent4, { anchor:[ 0.5, 1, 0, 1 ] }, exampleEndpoint1);

let exampleDropOptions2 = {
    tolerance: "touch",
    hoverClass: "dropHover",
    activeClass: "dragActive"
};

let exampleEndpoint2 = {
    endpoint: { type: "Dot", options: { radius: 5 } },
    paintStyle: { fill: "green" },
    maxConnections: -1,
    source: false,
    target: true,
    connectionsDetachable: false,
};

let sourceEndpointChild1 = instance.addEndpoint(child1, { anchor:[ 0.5, 0, 0, -1 ] }, exampleEndpoint2);
let sourceEndpointChild2 = instance.addEndpoint(child2, { anchor:[ 0.5, 0, 0, -1 ] }, exampleEndpoint2);