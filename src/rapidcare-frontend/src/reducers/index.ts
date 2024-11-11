import { combineReducers } from 'redux';
import pocReducer from './poc';


const rootReducer = combineReducers({
  poc: pocReducer,
  //future reducers  
});

export default rootReducer;
