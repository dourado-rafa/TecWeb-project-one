let xhr = new XMLHttpRequest()

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomStyle(card) {
  card.className += ` card-color-${getRandomInt(1, 5)} card-rotation-${getRandomInt(1, 11)}`;
}

function stringToElement(string) {
  let template = document.createElement('template')
  template.innerHTML = string
  return template.content.firstChild
}

document.addEventListener("DOMContentLoaded", function () {
  // Sorteia classes de cores aleatoriamente para os cards
  let cards = document.getElementsByClassName("card");
  for (let i = 0; i < cards.length; i++) {
    let card = cards[i];
    randomStyle(card)
  }
});

function createNote() {
  xhr.open('POST', `/create`, true)
  xhr.onload = function (e) {
    if (xhr.status == 200) {
      let card = stringToElement(xhr.response)
      randomStyle(card)
      document.getElementById('notes-list').appendChild(card)
    } else {
      console.log(`A tentativa de criar essa nota falhou!`)
    }
  }
  let title = document.getElementById('card-title')
  let content = document.getElementById('card-content')
  xhr.send(`title=${title.value}&content=${content.value}`)
  title.value = ''
  content.value = ''
}

function deleteNote(id) {
  xhr.open('GET', `/delete/${id}`, true)
  xhr.onload = function (e) {
    if (xhr.status == 200) {
      let note = document.getElementById(`note-${id}`)
      note.parentNode.removeChild(note)
    } else {
      console.log(`A tentativa de apagar a nota ${id} falhou!`)
    }
  }
  xhr.send()
}

