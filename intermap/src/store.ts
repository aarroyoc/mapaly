import { createSlice, createStore, PayloadAction } from "@reduxjs/toolkit";

import {QuizState, Question, cleanupQuestion} from "./models";

const initialState: QuizState = {
    score: 0,
    questions: [],
    time: new Date(),
    activeQuestion: null,
};

function selectQuestion(state: QuizState): void{
    let answers = state.questions.filter((question)=> !question.done);
    if(answers.length > 0){
        let rnd = Math.floor(Math.random() * answers.length);
        state.activeQuestion = answers[rnd];
    }else{
        state.activeQuestion = null;
    }
}

const slice = createSlice({
    name: "quiz",
    initialState,
    reducers: {
        setQuestions: (state: QuizState, action: PayloadAction<Question[]>) => {
            state.questions = action.payload;
            selectQuestion(state);      
        },
        submitAnswer: (state: QuizState, action: PayloadAction<string>) => {
            if(action.payload === state.activeQuestion?.answer){
                state.activeQuestion.done = true;
                selectQuestion(state);
                state.score += 25;
            }else{
                state.score = Math.max(0, state.score-10);
            }
        }
    }
});

export const actions = slice.actions;

const store = createStore(slice.reducer);

export default store;