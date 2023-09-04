//jQuery variables start with dollar sign!
"use strict";

let $cupcakeList = $('.cupcake-list');
let $cupcakeForm = $('.add-cupcake-form');
let $searchForm = $('.search-cupcakes-form');

$cupcakeForm.on('submit', handleNewCupcake);
$searchForm.on('submit', handleSearch);
/**
 * Gets initial cupcake list, then displays it.
 */
async function start() {

  let response = await fetch('/api/cupcakes'); //get, nothing more needed.
  let cupcakeData = await response.json();
  //console.log(cupcakeData);

  displayCupcakes(cupcakeData.cupcakes);
}

/**
 * submits POST request to API to add cupcake to database.
 * (Refreshed page should included new cupcake).
 * @param {*} evt
 */
//FIXME: update so that we don't need to refresh page.
//can check about triggering reset on form? jQuery
async function handleNewCupcake(evt) {
  evt.preventDefault();

  //get cupcake data from form:
  let newCupcake = {
    'flavor': $('#flavor').val(),
    'size': $('#size').val(),
    'rating': $('#rating').val(),
    'image_url': $('#image_url').val()
  };

  //add new cupcake via API:
  let response = await fetch('/api/cupcakes', {
    method: "POST",
    body: JSON.stringify(newCupcake),
    headers: { "Content-type": "application/json" }
  });
  let parsed = await response.json();
  console.log(parsed);


  //Clear form inputs
  $cupcakeForm.find("input[type=text], input[type=number]").val("");


  //Redraw page
  response = await fetch('/api/cupcakes'); //get, nothing more needed.
  let cupcakeData = await response.json();

  displayCupcakes(cupcakeData.cupcakes);
}




/**
 * Redraws page with smaller list matching search params.
 * @param {*} evt
 */
async function handleSearch(evt){
  evt.preventDefault();

  let searchTerm = $('.search_term').val();
  let params = new URLSearchParams({'search_term': searchTerm});

  let response = await fetch(`/api/cupcakes/search?${params}`);
  let cupcakeData = await response.json();

  console.log('cupcake data is: ', cupcakeData.cupcakes);
  displayCupcakes(cupcakeData.cupcakes);
}





/**
 * Loops through cupcake data received from API, and builds a list
 * of cupcake card elements to display.
 * @param {*} cupcakeData
 */
async function displayCupcakes(cupcakeData) {

  console.log('got to display cupcakes');
  console.log('data is : ', cupcakeData);
  //Add to $cupcakeList
  $cupcakeList.empty();

  for (let cupcake of cupcakeData) {
    let cupcakeCard = $(`<li>
      <img src="${cupcake.image_url}" class="cupcake-card-img">
      <p>Flavor: ${cupcake.flavor} <br>
      Size: ${cupcake.size} <br>
      Rating: ${cupcake.rating}</p>`);
    $cupcakeList.append(cupcakeCard);
  }
}

start();