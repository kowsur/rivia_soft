const { useState } = React;

function TodoApp() {
  const [items, setItems] = useState([]);

  function handleSubmit(event) {
    event.preventDefault();
    const text = event.target.elements.todo.value;
    const newItems = [...items, { text }];
    setItems(newItems);
    event.target.reset();
  }

  return (
    <div>
      <h1>Todo App</h1>
      <form onSubmit={handleSubmit}>
        <input name="todo" placeholder="Enter task" />
        <button>Add</button>
      </form>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item.text}</li>
        ))}
      </ul>
    </div>
  );
}

ReactDOM.render(<TodoApp />, document.getElementById("root"));
