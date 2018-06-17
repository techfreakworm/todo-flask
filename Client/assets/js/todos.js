window.onload = function() {

  const inputText = document.querySelector("#input-text");
  const delDone = document.querySelector("#del-done");
  const todoListHtml = document.querySelector("#todolist");

  //XTODO: call GET all todos api here
  let myTodoList = {};
  $.ajax({
    url: "http://127.0.0.1:5000/todos/",
    method: "GET",
    success: function(data) {
      myTodoList.todos = data;
      drawTodoListAgain();
    }
  })

  inputText.addEventListener("keypress", function(event) {
    if (event.which === 13 && inputText.value) {
      //XTODO: call POST api here
      $.ajax({
        url: "http://127.0.0.1:5000/todos/",
        method: "POST",
        data: {
          text: inputText.value
        },
        success: function() {
          $.ajax({
            url: "http://127.0.0.1:5000/todos/",
            method: "GET",
            success: function(data) {
              myTodoList.todos = data;
              drawTodoListAgain();
            }
          })
          drawTodoListAgain();
        }
      })

      inputText.value = "";
    }
  });

  delDone.addEventListener("click", function() {
    myTodoList.removeDoneTodos();
    drawTodoListAgain();
  });

  function drawTodoListAgain() {
    todoListHtml.innerHTML = "";
    let flag = false;
    myTodoList.todos.forEach(function(todo) {
      flag = todo.done || flag;
      addToDoHtml(todo.text, todo.done, todo.id)
    })
  }

  function addToDoHtml(todoText, todoDone, todoId) {
    let newListItem = document.createElement("li");

    let innerHtml = "";

    if(todoDone) {
      innerHtml += `
        <input class = "todo-done" data-target="todo-done" type="checkBox" checked>
        <span class="todo-text completed" data-target="todo-text">${todoText}</span>
      `;
    } else {
      innerHtml += `
        <input class = "todo-done" data-target="todo-done" type="checkBox">
        <span class="todo-text" data-target="todo-text">${todoText}</span>
      `;
    }

    innerHtml += `
      <span class="todo-grow"></span>
      <i class="fa fa-trash todo-del" aria-hidden="true" data-target="todo-delete"></i>
    `;

    newListItem.innerHTML = innerHtml;
    newListItem.setAttribute("data-id", todoId);
    newListItem.addEventListener("click", liClickEvent);
    todoListHtml.appendChild(newListItem);
  }

  function liClickEvent(event) {
    const todo = myTodoList.todos.filter(todo => todo.id == event.currentTarget.getAttribute("data-id"))[0]

    switch (event.target.getAttribute("data-target")) {
      case "todo-done":
        //XTODO: call PUT api here
        $.ajax({
          url: `http://127.0.0.1:5000/todos/${todo.id}/`,
          method: "PUT",
          data: {
            text: todo.text,
            done: !todo.done
          },
          success: function() {
            $.ajax({
              url: "http://127.0.0.1:5000/todos/",
              method: "GET",
              success: function(data) {
                myTodoList.todos = data;
                drawTodoListAgain();
              }
            })
          }
        })
        break;
      case "todo-delete":
        //XTODO: call DELETE api here
        $.ajax({
          url: `http://127.0.0.1:5000/todos/${todo.id}/`,
          method: "DELETE",
          success: function() {
            $.ajax({
              url: "http://127.0.0.1:5000/todos/",
              method: "GET",
              success: function(data) {
                myTodoList.todos = data;
                drawTodoListAgain();
              }
            })
          }
        })
        break;
    }
  }

};
