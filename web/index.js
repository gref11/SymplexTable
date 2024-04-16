let table = document.querySelector("table");
let container = document.querySelector(".container");
let form = document.querySelector("form");
let nInput = document.querySelector(".n");
let mInput = document.querySelector(".m");
let pInput = document.querySelector(".p");
let aInput = document.querySelectorAll(".a");
let cInput = document.querySelectorAll(".c");
let aTable = document.querySelector(".A");
let cTable = document.querySelector(".C");
let clTable = document.querySelector(".c-l");
let submit = document.querySelector(".submit");
let clean = document.querySelector(".clean");
let solution = document.querySelector(".solution");

// var n = 5;
// var m = 3;
// var p = false;
// var a = [];
// for (let i = 0; i < m; i++) {
//   a.push([]);
//   for (let j = 0; j < n + 1; j++) {
//     a[i].push(0);
//   }
// }
// var c = [];
// var cl = [];
// for (let i = 0; i < n; i++) {
//   c.push(0);
//   cl.push(0);
// }

var c = [5, -1, 2, 1, -1];
var cl = [-3, 3, -4, -3, 3];
var p = true;
var n = 5;
var m = 3;
var a = [
  [-86, -2, 1, -17, -5, 1],
  [-2, 0, 1, -11, 1, -1],
  [-61, -1, -1, 5, -4, -1],
];

function clean_container() {
  container.innerHTML = "";
}

function createA() {
  str = ``;
  str = "<h4>Ограничения</h4>";
  for (let i = 0; i < m; i++) {
    str += `<div><input class="a no-spin-button" name="a" type="number" value=${a[i][0]}></div>=`;
    for (let j = 0; j < n; j++) {
      str += `<div><input class="a no-spin-button" name="a" type="number" value=${
        a[i][j + 1]
      }></div>`;
    }
    str += `<br>`;
  }
  aTable.innerHTML = str;
  aInput = document.querySelectorAll(".a");
  for (let i = 0; i < aInput.length; i++) {
    aInput[i].addEventListener("change", function (event) {
      for (let j = 0; j < aInput.length; j++) {
        a[Math.floor(j / (n + 1))][j % (n + 1)] = Number(aInput[j].value);
      }
    });
  }
}

function createC() {
  str = ``;
  str += `<h4>Целевая функция</h4>C' = `;
  for (let j = 0; j < n; j++) {
    str += `<div><input class="c no-spin-button" name="c" type="number" value=${c[j]}></div>`;
  }
  str += `<br><div class="c-l ${p ? "" : "hidden"}">C" = `;
  for (let j = 0; j < n; j++) {
    str += `<div><input class="c no-spin-button" name="c" type="number" value=${cl[j]}></div>`;
  }
  str += `</div><br>`;
  cTable.innerHTML = str;
  clTable = document.querySelector(".c-l");
  cInput = document.querySelectorAll(".c");
  for (let i = 0; i < cInput.length; i++) {
    cInput[i].addEventListener("change", function (event) {
      for (let j = 0; j < cInput.length; j++) {
        if (j < n) {
          c[j] = Number(cInput[j].value);
        } else cl[j - n] = Number(cInput[j].value);
      }
      console.log(c, cl);
    });
  }
}

async function solve(event) {
  event.preventDefault();
  console.log(123);
  let solution;
  if (p) solution = await eel.solve(n, m, c, a, cl)();
  else solution = await eel.solve(n, m, c, a)();
  // create_form();
  add_solve(solution);
}

function cleanTask(event) {
  event.preventDefault();
  n = 5;
  m = 3;
  a = [];
  c = [];
  cl = [];
  for (let i = 0; i < m; i++) {
    a.push([]);
    for (let j = 0; j < n + 1; j++) {
      a[i].push(0);
    }
  }
  for (let i = 0; i < n; i++) {
    c.push(0);
    cl.push(0);
  }
  createA();
  createC();
  solution.innerHTML = "";
}

function create_form() {
  str = `<form>
  <label for="n">Количество переменных</label>
  <div><input class="n" name="n" type="number" value=5 min=1></div>
  <br>
  <label for="m">Количество ограничений</label>
  <div><input class="m" name="m" type="number" value=3 min=1></div>
  <br>
  <label for="p">Параметр</label>
  <div class="checkbox"><input type="checkbox" class="p" name="p" checked=${p}></div>
  <br>
  <div class="A"></div><br>
  <div class="C"></div>
  <br>
  <br>
  </form>
  <button class="submit">Решить</button> <button class="clean">Очистить</button>
  <br>
  <div class="solution"></div>
  `;
  container.insertAdjacentHTML("beforeend", str);

  nInput = document.querySelector(".n");
  mInput = document.querySelector(".m");
  pInput = document.querySelector(".p");
  aTable = document.querySelector(".A");
  cTable = document.querySelector(".C");
  submit = document.querySelector(".submit");
  form = document.querySelector("form");
  solution = document.querySelector(".solution");
  clean = document.querySelector(".clean");

  createA();
  createC();
  nInput.addEventListener("change", function (event) {
    n = Number(event.target.value);
    a_ = a;
    a = [];
    for (let i = 0; i < m; i++) {
      a.push([]);
      for (let j = 0; j < n + 1; j++) {
        a[i].push(0);
      }
    }
    for (let i = 0; i < Math.min(a_.length, a.length); i++)
      for (let j = 0; j < Math.min(a_[0].length, a[0].length); j++)
        a[i][j] = a_[i][j];
    c_ = c;
    c = [];
    for (let i = 0; i < n; i++) c.push(0);
    for (let i = 0; i < Math.min(c_.length, c.length); i++) c[i] = c_[i];
    cl_ = cl;
    cl = [];
    for (let i = 0; i < n; i++) cl.push(0);
    for (let i = 0; i < Math.min(cl_.length, cl.length); i++) cl[i] = cl_[i];
    createA();
    createC();
  });
  mInput.addEventListener("change", function (event) {
    m = Number(event.target.value);
    a_ = a;
    a = [];
    for (let i = 0; i < m; i++) {
      a.push([]);
      for (let j = 0; j < n + 1; j++) {
        a[i].push(0);
      }
    }
    for (let i = 0; i < Math.min(a_.length, a.length); i++)
      for (let j = 0; j < Math.min(a_[0].length, a[0].length); j++)
        a[i][j] = a_[i][j];
    createA();
  });

  pInput.addEventListener("change", function (event) {
    p = event.target.checked;
    clTable.classList.toggle("hidden");
  });

  submit.addEventListener("click", solve);
  clean.addEventListener("click", cleanTask);
}

function add_solve(x) {
  solution.innerHTML = x;
}

clean_container();
create_form();
