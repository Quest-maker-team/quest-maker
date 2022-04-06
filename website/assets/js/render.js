export function RenderBlock(id, content){
    let block = document.createElement("div");
    block.id = id;
    block.className = "position-absolute border-2 card";

    let blockBody = document.createElement("div");
    blockBody.className = "card-body";
    blockBody.innerHTML = content;
    block.style.width = "10rem";

    block.append(blockBody);

    document.getElementById("container").append(block);
    return block;
}

export function RenderStart(question, instance, sourceEndpoint){
    let content = "<h5 class=\"card-title text-center\">Start</h5>" +
                    "<hr>" +
                    "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
    let block = RenderBlock(question.question_id, content);
    instance.manage(block, block.id);
    instance.addEndpoint(block, sourceEndpoint);
}

export function RenderFinish(question, instance, targetEndpoint){
    let content = "<h5 class=\"card-title text-center\">Finish</h5>" +
                    "<hr>" +
                    "<p class=\"card-text text-center text-truncate\">"+ question.text +"</p>";
    let block = RenderBlock(question.question_id, content);
    instance.manage(block, block.id);
    instance.addEndpoint(block, targetEndpoint);
}

export function Render(quest, instance, sourceEndpoint, targetEndpoint) {
    RenderStart(quest.questions.find(question => question.type === "start"), instance, sourceEndpoint);
    RenderFinish(quest.questions.find(question => question.type === "end"), instance, targetEndpoint);
}