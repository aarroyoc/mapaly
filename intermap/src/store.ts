import { createSlice, createStore, PayloadAction } from "@reduxjs/toolkit";

import {QuizState, Question, cleanupQuestion} from "./models";

const initialState: QuizState = {
    score: 0,
    questions: [],
    time: 0,
    activeQuestion: null,
};

function selectQuestion(state: QuizState): void{
    const answers = state.questions.filter((question)=> !question.done);
    if(answers.length > 0){
        const rnd = Math.floor(Math.random() * answers.length);
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
                state.activeQuestion.done = true; // TODO: Why doesn't work?
                for(let qst of state.questions){
                    if(qst.question === state.activeQuestion.question){
                        qst.done = true;
                    }
                }
                selectQuestion(state);
                state.score += 25;
            }else{
                state.score = Math.max(0, state.score-10);
            }
        },
        tick: (state: QuizState) => {
            if(state.activeQuestion){
                state.time += 1;
            }
        }
    }
});

export const actions = slice.actions;

const store = createStore(slice.reducer);

export default store;