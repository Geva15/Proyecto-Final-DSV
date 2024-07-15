document.addEventListener('DOMContentLoaded', () => {
    console.log("Documento cargado");
    const notas = localStorage.getItem('notasCancion');
    if (notas) {
        console.log("Notas cargadas desde localStorage:", notas);
        const notesSequence = JSON.parse(notas);
        let currentNoteIndex = 0;
        let isSongStarted = false;

        function playNoteOnPiano(note) {
            const audio = new Audio(`/static/notas/${note}.wav`);
            audio.play().then(() => {
                console.log(`Played note: ${note}`);
            }).catch(error => {
                console.error(`Error playing note: ${note}`, error);
            });
        }

        function highlightNoteOnStaff(noteIndex) {
            const pentagrama = document.querySelector('.pentagrama');
            const notes = pentagrama.querySelectorAll('.nota');
            notes.forEach((nota, index) => {
                nota.classList.remove('highlight-blue', 'highlight-blue-do');
                if (index === noteIndex % 10) {
                    if (notesSequence[noteIndex] === 'do') {
                        nota.classList.add('highlight-blue-do');
                    } else {
                        nota.classList.add('highlight-blue');
                    }
                }
            });
        }

        function checkNotePlayed(note) {
            if (!isSongStarted) return;
            console.log(`Checking note played: ${note}`);
            if (note === notesSequence[currentNoteIndex]) {
                currentNoteIndex++;
                if (currentNoteIndex < notesSequence.length) {
                    updateNotesOnStaff();
                    highlightNoteOnStaff(currentNoteIndex);
                } else {
                    alert("¡Felicidades! Has completado la canción.");
                    isSongStarted = false;
                }
            } else {
                const keyElement = document.querySelector(`.key[data-note="${note}"]`);
                keyElement.classList.add('wrong');
                setTimeout(() => {
                    keyElement.classList.remove('wrong');
                }, 500);
            }
        }

        function createNotesOnStaff() {
            const pentagrama = document.querySelector('.pentagrama');
            pentagrama.innerHTML = '<img src="/static/imagenes/claveSol.png" alt="Clave sol" class="clave">';
            const startIndex = Math.floor(currentNoteIndex / 10) * 10;
            for (let i = startIndex; i < startIndex + 10 && i < notesSequence.length; i++) {
                const note = notesSequence[i];
                const noteElement = document.createElement('img');
                noteElement.src = `/static/imagenes/${note}.png`;
                noteElement.alt = note.charAt(0).toUpperCase() + note.slice(1);
                noteElement.className = `nota ${note}`;
                noteElement.style.left = `${(i - startIndex) * 60 + 100}px`;
                noteElement.setAttribute('data-nombre', note);
                noteElement.setAttribute('data-sonido', `${note}.wav`);
                pentagrama.appendChild(noteElement);
            }
        }

        function updateNotesOnStaff() {
            const pentagrama = document.querySelector('.pentagrama');
            pentagrama.innerHTML = '';
            createNotesOnStaff();
        }

        document.querySelectorAll('.key').forEach(key => {
            key.addEventListener('click', () => {
                const note = key.getAttribute('data-note');
                console.log(`Key pressed: ${note}`);
                playNoteOnPiano(note);
                key.classList.add('pressed');
                setTimeout(() => {
                    key.classList.remove('pressed');
                }, 100);
                checkNotePlayed(note);
            });
        });

        document.getElementById('start-song').addEventListener('click', () => {
            isSongStarted = true;
            currentNoteIndex = 0;
            updateNotesOnStaff();
            highlightNoteOnStaff(currentNoteIndex);
            console.log("Canción iniciada");
        });
    } else {
        console.error("No se encontraron notas en el localStorage");
    }
});