export class BlockRedactor {
    static createStartRedactor(question){
        document.getElementById("redactorForm").innerHTML = "<label for=\"formControlTextarea\"" +
            " class=\"form-label\">Приветственное сообщение:</label>" +
            "<textarea class=\"form-control\" id=\"formControlTextarea\" rows=\"3\"> " +
            question.text +
            "</textarea>";
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static createFinishRedactor(question){
        document.getElementById("redactorForm").innerHTML = "<label for=\"formControlTextarea\"" +
            " class=\"form-label\">Прощальное сообщение:</label>" +
            "<textarea class=\"form-control\" id=\"formControlTextarea\" rows=\"3\" >" +
            question.text +
            "</textarea>";
        document.getElementById("update").onclick = () => {
            question.text = document.getElementById("formControlTextarea").value;
            document.getElementById(question.question_id).getElementsByClassName("card-text")[0].textContent =
                question.text;
        };
    }

    static createOpenQuestionRedactor(){

    }

    static createMovementRedactor(){

    }

    static showRedactor(question){
        let modal = new bootstrap.Modal(document.getElementById("redactor"));
        switch (question.type) {
            case "start":
                this.createStartRedactor(question);
                break;
            case "end":
                this.createFinishRedactor(question);
                break;
            default:
                break;
        }
        modal.show();
    }
}