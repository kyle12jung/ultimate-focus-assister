// States
// todo format { text: "", completed = True }
let APP_STATE = {
    totalItems: 0,
    todo: [],
}

// reducer
const reducer = (state = [], action) => {
    console.log("reducer", state, action);
    switch (action.type) {
        case 'ADD_TODO':
            return [...state, { text: action.payload, completed: false }]
    }

}
const store = Redux.createStore(reducer);

// Elements
const todos = document.querySelector('.todos');
const completed = document.querySelector('.completed');
const userInput = document.querySelector('.user-input');
const addButton = document.querySelector('.add');

// dispatch is similar to setState (in react, onClick setState)
addButton.addEventListener("click", () => {
    store.dispatch({ type: "ADD_TODO", payload: userInput.value });
})

// subscribe (sort of like useEffect)
store.subscribe(() => {
    todos.innerHTML = "";
    userInput.value = "";
    store.getState().forEach((todo) => {
        const span = document.createElement('span');
        const checkBox = document.createElement("input");
        checkBox.setAttribute("type", "checkbox");
        const todoText = document.createElement('p');
        todoText.innerText = todo.text;
        span.appendChild(checkBox);
        span.appendChild(todoText)
        todos.appendChild(span)
    })
})