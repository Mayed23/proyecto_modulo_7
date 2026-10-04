document.addEventListener('DOMContentLoaded', () => {
    const formatoCLP = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' });

    // ============================
    // Selector de cuentas (cuando el cliente tiene varias)
    // ============================
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

    // ============================
    // Buscador simple para el campo de clientes (formulario de Cuenta)
    // ============================
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

    // ============================
    // Mostrar saldo disponible al elegir cuenta (formulario de Transacción)
    // ============================
    const selectCuenta = document.getElementById('id_cuenta');
    const saldoTexto = document.getElementById('saldo_disponible');

    if (selectCuenta && saldoTexto && typeof saldosPorCuenta !== 'undefined') {
        function actualizarSaldo() {
            const idSeleccionado = selectCuenta.value;
            const saldo = saldosPorCuenta[idSeleccionado];
            if (saldo !== undefined) {
                saldoTexto.textContent = `Saldo disponible: ${formatoCLP.format(saldo)}`;
            } else {
                saldoTexto.textContent = '';
            }
        }

        selectCuenta.addEventListener('change', actualizarSaldo);
        actualizarSaldo(); // muestra el saldo si ya hay una cuenta preseleccionada
    }
});