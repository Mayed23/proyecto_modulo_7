document.addEventListener('DOMContentLoaded', () => {
    const formatoCLP = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' });


    document.querySelectorAll('.aw-cuenta-selector').forEach(grupo => {
        const botones = grupo.querySelectorAll('.btn-cuenta');
        const card = grupo.closest('.aw-card');
        const saldoEl = card.querySelector('.aw-saldo-cliente');

        function animarSaldo(target) {
            let current = 0;
            const increment = target / 30 || 0;
            clearInterval(saldoEl._timer);
            saldoEl._timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    current = target;
                    clearInterval(saldoEl._timer);
                }
                saldoEl.textContent = formatoCLP.format(current);
            }, 15);
        }

        function seleccionar(boton) {
            botones.forEach(b => b.classList.remove('is-selected'));
            boton.classList.add('is-selected');
            animarSaldo(parseFloat(boton.dataset.saldo));
        }

        botones.forEach(boton => {
            boton.addEventListener('click', () => seleccionar(boton));
        });
    });

    const buscador = document.getElementById('buscador_clientes');
    const selectClientes = document.getElementById('id_clientes');

    if (buscador && selectClientes) {
        buscador.addEventListener('input', () => {
            const texto = buscador.value.toLowerCase();
            Array.from(selectClientes.options).forEach(opcion => {
                const coincide = opcion.textContent.toLowerCase().includes(texto);
                opcion.hidden = !coincide;
            });
        });
    }
});