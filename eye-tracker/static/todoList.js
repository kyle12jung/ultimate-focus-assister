// reducer
const reducer = (state = [], action) => {
    console.log("reducer", state, action);
    switch (action.type) {
        case 'ADD_TODO':
            return [...state, { text: action.payload.value, completed: false }]
        case 'TOGGLE_TODO':
            return state.map(todo => {
                // If this isn't the todo item we're looking for, leave it alone
                if (todo.text !== action.payload.value) {
                    return todo
                }

                // We've found the todo that has to change. Return a copy:
                return {
                    ...todo,
                    // Flip the completed flag
                    completed: !todo.completed
                }
            })
    }
}
const store = Redux.createStore(reducer);

// Elements
const todos = document.querySelector('.todos');
const completed = document.querySelector('.completed');
const userInput = document.querySelector('.user-input');
const addButton = document.querySelector('.add');

// helper function to add multiple attributes to an element
function setAttributes(el, attrs) {
    for (let key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}

// dispatch is similar to setState (in react, onClick setState)
addButton.addEventListener("click", (evt) => {
    store.dispatch({ type: "ADD_TODO", payload: { value: userInput.value } });
})

const toggleCheckbox = (text) => {
    console.log(text);
    store.dispatch({ type: "TOGGLE_TODO", payload: { value: text } });
}

// subscribe (sort of like useEffect)
store.subscribe(() => {
    todos.innerHTML = null;
    userInput.value = "";
    store.getState().forEach((todo, i) => {
        const span = document.createElement('span');
        todos.appendChild(span);
        setAttributes(span, { "class": "todo", "id": i });
        const checkBox = document.createElement("input");
        span.appendChild(checkBox);
        setAttributes(checkBox, { "type": "checkbox", "class": "checkbox" });
        const todoText = document.createElement('p');
        todoText.innerText = todo.text;
        span.appendChild(todoText);
        checkBox.addEventListener("click", () => toggleCheckbox(todoText.innerText));
    })
})