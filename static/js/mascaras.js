/*
 * Máscaras simples para inputs, sem bibliotecas.
 * Uso: <input type="text" data-mask="cpf">
 * Tipos: cpf, cnpj, telefone, data, cep
 */
(function () {
    // "0" = um dígito; qualquer outro caractere é fixo
    var padroes = {
        cpf: "000.000.000-00",
        cnpj: "00.000.000/0000-00",
        data: "00/00/0000",
        cep: "00000-000"
    };

    function escolherPadrao(tipo, digitos) {
        if (tipo === "telefone") {
            // 11 dígitos = celular; até 10 = fixo
            return digitos.length > 10 ? "(00) 00000-0000" : "(00) 0000-0000";
        }
        return padroes[tipo];
    }

    function formatar(valor, tipo) {
        var digitos = valor.replace(/\D/g, "");
        var padrao = escolherPadrao(tipo, digitos);
        if (!padrao) return valor;

        var resultado = "";
        var i = 0;

        for (var k = 0; k < padrao.length; k++) {
            if (i >= digitos.length) break;
            if (padrao[k] === "0") {
                resultado += digitos[i++];
            } else {
                resultado += padrao[k];
            }
        }
        return resultado;
    }

    function ativar(input) {
        var tipo = input.dataset.mask;
        var maximo = tipo === "telefone" ? 15 : (padroes[tipo] || "").length;

        if (maximo) input.maxLength = maximo;
        input.setAttribute("inputmode", "numeric");

        input.addEventListener("input", function () {
            input.value = formatar(input.value, tipo);
        });

        // Formata valores que já vêm preenchidos (ex.: tela de edição)
        if (input.value) input.value = formatar(input.value, tipo);
    }

    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll("[data-mask]").forEach(ativar);
    });
})();