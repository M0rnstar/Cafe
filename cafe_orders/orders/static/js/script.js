// Ждём загрузки страницы
document.addEventListener("DOMContentLoaded", function () {
  var addDishButton = document.getElementById("add-dish-button");
  var dishNameInput = document.getElementById("dish_name_input");
  var dishPriceInput = document.getElementById("dish_price_input");
  var dishesTableBody = document.querySelector("#dishes-table tbody");
  var hiddenDishesDiv = document.getElementById("hidden-dishes");

  // Счётчик для уникальных идентификаторов блюд
  var dishCount = 0;

  addDishButton.addEventListener("click", function (e) {
    e.preventDefault();
    var dishName = dishNameInput.value.trim();
    var dishPrice = dishPriceInput.value.trim();

    if (dishName === "" || dishPrice === "") {
      alert("Пожалуйста, заполните и название блюда, и цену.");
      return;
    }

    // Создаём уникальный идентификатор для блюда
    var dishId = "dish-" + dishCount;
    dishCount++;

    // Создаём строку таблицы для отображения блюда
    var tr = document.createElement("tr");
    tr.setAttribute("data-dish-id", dishId);

    var tdName = document.createElement("td");
    tdName.textContent = dishName;
    var tdPrice = document.createElement("td");
    tdPrice.textContent = dishPrice;
    var tdActions = document.createElement("td");

    // Создаём кнопку для удаления блюда
    var deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.textContent = "Удалить";
    deleteButton.addEventListener("click", function () {
      // Удаляем строку таблицы
      tr.remove();
      // Удаляем соответствующий скрытый блок
      var hiddenDish = document.querySelector(
        '.hidden-dish[data-dish-id="' + dishId + '"]'
      );
      if (hiddenDish) {
        hiddenDish.remove();
      }
    });
    tdActions.appendChild(deleteButton);

    tr.appendChild(tdName);
    tr.appendChild(tdPrice);
    tr.appendChild(tdActions);
    dishesTableBody.appendChild(tr);

    // Создаём скрытый блок для передачи данных о блюде на сервер
    var hiddenContainer = document.createElement("div");
    hiddenContainer.classList.add("hidden-dish");
    hiddenContainer.setAttribute("data-dish-id", dishId);

    // Скрытое поле для названия блюда
    var hiddenDishName = document.createElement("input");
    hiddenDishName.type = "hidden";
    hiddenDishName.name = "dish_name";
    hiddenDishName.value = dishName;
    // Скрытое поле для цены блюда
    var hiddenDishPrice = document.createElement("input");
    hiddenDishPrice.type = "hidden";
    hiddenDishPrice.name = "dish_price";
    hiddenDishPrice.value = dishPrice;

    hiddenContainer.appendChild(hiddenDishName);
    hiddenContainer.appendChild(hiddenDishPrice);
    hiddenDishesDiv.appendChild(hiddenContainer);

    // Очищаем поля ввода для следующего блюда
    dishNameInput.value = "";
    dishPriceInput.value = "";
  });
});
