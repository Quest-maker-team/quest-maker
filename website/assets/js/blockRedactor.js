export class BlockRedactor {
    static addTextRedactor(form, label, text){
        form.innerHTML +=
            "<label for=\"formControlTextarea\" class=\"form-label\">" + label + "</label>" +
            "<textarea class=\"form-control\" id=\"formControlTextarea\" rows=\"3\"> " +
            text +
            "</textarea>";
    }

    static addAnswerForOpenQuestion(form, answer){
        form.innerHTML +=
            "<div class='col-8'>"+
                "<input type=\"text\" class=\"form-control\" id=\"answerText\" value=" + answer.text + ">" +
            "</div>" +
            "<div class=\"col-3\">" +
                "<div class='input-group'>" +
                    "<span class=\"input-group-text\"> Очки </span>" +
                    "<input type=\"text\" class=\"form-control\" id=\"answerPoints\" value=" + answer.points + ">" +
                "</div>" +
            "</div>" +
            "<div class='col-1'>" +
                "<button class=\"btn btn-danger\">-</button>" +
            "</div>"
    }

    static createStartRedactor(form, question){
        this.addTextRedactor(form, "Приветственное сообщение:", question.text);
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static createFinishRedactor(form, question){
        this.addTextRedactor(form, "Прощальное сообщение:", question.text);
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static createOpenQuestionRedactor(form, question){
        this.addTextRedactor(form, "Вопрос", question.text);
        form.innerHTML += "<hr><label for=\"formControlTextarea\" class=\"form-label\">Ответы:</label>";
        for (let answer of question.answer_options) {
            this.addAnswerForOpenQuestion(form, answer);
        }
        form.innerHTML += "<div class='col-auto'><button type='button' class='btn btn-primary'>Добавить ответ</button></div>";
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
            let answerTable = document.getElementById(question.question_id).getElementsByTagName("li");

        };
    }

    static createMovementRedactor(form, question){
        this.addTextRedactor(form, "Перемещение", question.text);
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static showRedactor(question){
        let modal = new bootstrap.Modal(document.getElementById("redactor"));
        let form = document.getElementById("redactorForm");
        form.innerHTML = "";
        switch (question.type) {
            case "start":
                this.createStartRedactor(form, question);
                break;
            case "end":
                this.createFinishRedactor(form, question);
                break;
            case "open":
                this.createOpenQuestionRedactor(form, question);
                break;
            case "movement":
                this.createMovementRedactor(form, question);
                break;
            default:
                break;
        }

        modal.show();
    }
}