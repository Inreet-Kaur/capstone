import { createStore, applyMiddleware, AnyAction } from 'redux';
import { thunk, ThunkDispatch } from 'redux-thunk';
import { AppState } from './reducers/AppState';
import rootReducer from './reducers';


export type AppDispatch = ThunkDispatch<AppState, unknown, AnyAction>;

const store = createStore(
    rootReducer,
    applyMiddleware(thunk)
);

export default store;



