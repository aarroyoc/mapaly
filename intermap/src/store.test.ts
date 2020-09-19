import { Question } from "./models";
import store from "./store";

const ANY_QUESTION_1: Question = {
    question: "Soria",
    answer: "soria",
    done: false
};

const ANY_QUESTION_2: Question = {
    question: "Palencia",
    answer: "palencia",
    done: true
};

const ANY_QUESTION_3: Question = {
    question: "Burgos",
    answer: "burgos",
    done: false,
};

test("setNewQuestions", () => {
    store.setQuestions([ANY_QUESTION_1, ANY_QUESTION_3]);
    store.selectQuestion();
    const question = store.activeQuestion;
    expect(question?.answer === "soria" || question?.answer === "burgos").toBe(true);
});

test("setQuestion already answered", () => {
    store.setQuestions([ANY_QUESTION_1, ANY_QUESTION_2]);
    store.selectQuestion();
    const question = store.activeQuestion;
    expect(question?.answer).toBe("soria");
});

test("submitOkAnswer", () => {
    ANY_QUESTION_1.done = false;
    store.score = 0;
    store.setQuestions([ANY_QUESTION_1]);
    store.selectQuestion();
    store.submitAnswer("soria");
    expect(store.score).toBe(25);
    store.selectQuestion();
    expect(store.activeQuestion).toBeNull();
});

test("submitBadAnswer", () => {
    ANY_QUESTION_1.done = false;
    store.score = 25;
    store.setQuestions([ANY_QUESTION_1]);
    store.selectQuestion();
    expect(store.activeQuestion).not.toBeNull();
    store.submitAnswer("burgos");
    expect(store.score).toBe(15);
    store.selectQuestion();
    expect(store.activeQuestion?.answer).toBe("soria");
});

test("tick/subscribe", () => {
    ANY_QUESTION_1.done = false;
    store.setQuestions([ANY_QUESTION_1]);
    store.selectQuestion();
    store.time = 0;
    const subscribeMock = jest.fn();
    store.subscribe(subscribeMock);
    store.tick();
    expect(store.time).toBe(1);
    expect(subscribeMock).toHaveBeenCalled();
});