document.addEventListener('DOMContentLoaded', () => {
    const formatoCLP = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' });

    document.querySelectorAll('.aw-cuenta-selector').forEach(grupo => {
        const botones = grupo.querySelectorAll('.btn-cuenta');
        const card = grupo.closest('.aw-card');
        const saldoEl = card.querySelector('.aw-saldo-cliente');
        const numeroEl = card.querySelector('.aw-numero-cuenta');

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
            botones.forEach(b => b.classList.remove('active'));
            boton.classList.add('active');
            numeroEl.textContent = boton.dataset.numero;
            animarSaldo(parseFloat(boton.dataset.saldo));
        }

        botones.forEach(boton => {
            boton.addEventListener('click', () => seleccionar(boton));
        });

    });
});