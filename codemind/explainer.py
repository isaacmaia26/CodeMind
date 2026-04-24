

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import List


@dataclass
class Finding:
    title: str
    beginner: str
    technical: str
    risk: int = 0


class CodeMindExplainer:
    """ Analisa o código e explica o que faz """

    def explain(self, source_code: str, mode: str = "beginner") -> str:
        source_code = source_code.strip()
        if not source_code:
            return "Cola algum código Python para eu analisar."

        try:
            tree = ast.parse(source_code)
        except SyntaxError as error:
            return (
                "Não consegui analisar este código porque existe um erro de sintaxe.\n\n"
                f"Linha {error.lineno}: {error.msg}"
            )

        findings = self._collect_findings(tree)

        if not findings:
            return (
                "Este código parece simples. Não encontrei funções, ciclos, classes ou estruturas complexas.\n"
                "Provavelmente executa instruções diretas, como atribuições ou chamadas simples."
            )

        total_risk = min(sum(item.risk for item in findings), 100)
        lines: List[str] = []
        lines.append("Analisei o teu código e encontrei isto:\n")

        for index, item in enumerate(findings, start=1):
            explanation = item.beginner if mode == "beginner" else item.technical
            lines.append(f"{index}. {item.title}\n   {explanation}\n")

        lines.append("\nResumo:")
	lines.append(self._build_summary(findings, total_risk))	
        return "\n".join(lines)

    def _collect_findings(self, tree: ast.AST) -> List[Finding]:
        findings: List[Finding] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                findings.append(Finding(
                    "Função encontrada",
                    f"O código cria uma função chamada '{node.name}', ou seja, um bloco reutilizável de lógica.",
                    f"FunctionDef '{node.name}' com {len(node.args.args)} argumento(s) e {len(node.body)} instrução(ões) internas.",
                ))

            elif isinstance(node, ast.AsyncFunctionDef):
                findings.append(Finding(
                    "Função assíncrona encontrada",
                    f"O código define uma função assíncrona chamada '{node.name}', usada para tarefas que podem esperar por resultados.",
                    f"AsyncFunctionDef '{node.name}' encontrado. Pode usar await, I/O assíncrono ou concorrência cooperativa.",
                ))

            elif isinstance(node, ast.ClassDef):
                findings.append(Finding(
                    "Classe encontrada",
                    f"O código cria uma classe chamada '{node.name}', normalmente usada para organizar dados e comportamentos.",
                    f"ClassDef '{node.name}' com {len(node.body)} elemento(s) no corpo da classe.",
                ))

            elif isinstance(node, ast.For):
                findings.append(Finding(
                    "Ciclo for encontrado",
                    "O código repete uma ação várias vezes, normalmente percorrendo uma lista, texto, range ou outro conjunto de dados.",
                    "Nó ast.For detetado. Existe iteração sobre um objeto iterável.",
                ))

            elif isinstance(node, ast.While):
                findings.append(Finding(
                    "Ciclo while encontrado",
                    "O código repete instruções enquanto uma condição continuar verdadeira.",
                    "Nó ast.While detetado. O fluxo depende de uma condição booleana dinâmica.",
                ))

            elif isinstance(node, ast.If):
                findings.append(Finding(
                    "Condição if encontrada",
                    "O código toma uma decisão: se uma condição for verdadeira, executa um bloco; caso contrário, pode executar outro.",
                    "Nó ast.If detetado. O programa possui ramificação condicional no fluxo de execução.",
                ))

            elif isinstance(node, ast.Try):
                findings.append(Finding(
                    "Tratamento de erros encontrado",
                    "O código tenta executar algo e está preparado para lidar com erros sem crashar imediatamente.",
                    "Nó ast.Try detetado. Existe tratamento de exceções com try/except/finally/else.",
                ))

            elif isinstance(node, ast.Import):
                names = ", ".join(alias.name for alias in node.names)
                findings.append(Finding(
                    "Biblioteca importada",
                    f"O código importa a biblioteca: {names}.",
                    f"Import direto detetado: {names}.",
                ))

            elif isinstance(node, ast.ImportFrom):
                module = node.module or "módulo relativo"
                names = ", ".join(alias.name for alias in node.names)
                findings.append(Finding(
                    "Importação específica encontrada",
                    f"O código importa {names} a partir de {module}.",
                    f"ImportFrom detetado: from {module} import {names}.",
                ))

            elif isinstance(node, ast.Call):
                call_name = self._get_call_name(node)
                if call_name == "print":
                    findings.append(Finding(
                        "Saída no terminal",
                        "O código mostra informação no ecrã usando print.",
                        "Chamada ast.Call para print() detetada.",
                    ))
                elif call_name in {"open", "Path.open"}:
                    findings.append(Finding(
                        "Acesso a ficheiros",
                        "O código abre ou manipula ficheiros no sistema.",
                        f"Chamada para {call_name} detetada. Pode ler ou escrever ficheiros dependendo dos argumentos.",
                        risk=10,
                    ))
                elif call_name in {"eval", "exec"}:
                    findings.append(Finding(
                        "Execução dinâmica perigosa",
                        "O código pode executar texto como se fosse código. Isto é poderoso, mas perigoso se receber dados externos.",
                        f"Chamada para {call_name} detetada. Execução dinâmica aumenta risco de segurança.",
                        risk=35,
                    ))
                elif call_name in {"system", "os.system", "subprocess.run", "subprocess.Popen", "subprocess.call"}:
                    findings.append(Finding(
                        "Execução de comandos do sistema",
                        "O código pode executar comandos no sistema operativo.",
                        f"Chamada para {call_name} detetada. Deve ser validada para evitar abuso.",
                        risk=30,
                    ))

            elif isinstance(node, ast.ListComp):
                findings.append(Finding(
                    "List comprehension encontrada",
                    "O código cria uma lista de forma compacta e elegante.",
                    "Nó ast.ListComp detetado. Construção funcional/compacta de listas.",
                ))

            elif isinstance(node, ast.DictComp):
                findings.append(Finding(
                    "Dict comprehension encontrada",
                    "O código cria um dicionário de forma compacta.",
                    "Nó ast.DictComp detetado. Construção compacta de dicionários.",
                ))

        return self._deduplicate(findings)

    def _get_call_name(self, node: ast.Call) -> str:
        func = node.func
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            parts = [func.attr]
            value = func.value
            while isinstance(value, ast.Attribute):
                parts.append(value.attr)
                value = value.value
            if isinstance(value, ast.Name):
                parts.append(value.id)
            return ".".join(reversed(parts))
        return "unknown"

    def _deduplicate(self, findings: List[Finding]) -> List[Finding]:
        seen = set()
        unique: List[Finding] = []
        for finding in findings:
            key = (finding.title, finding.beginner, finding.technical)
            if key not in seen:
                seen.add(key)
                unique.append(finding)
        return unique[:20]

    def _build_summary(self, findings: List[Finding], risk: int) -> str:
        has_function = any("Função" in f.title for f in findings)
        has_condition = any("Condição" in f.title for f in findings)
        has_loop = any("Ciclo" in f.title for f in findings)
        has_risk = risk > 0

        parts = []
        if has_function:
            parts.append("usa funções para organizar lógica")
        if has_condition:
            parts.append("toma decisões com condições")
        if has_loop:
            parts.append("repete ações com ciclos")
        if has_risk:
            parts.append(f"tem pontos que merecem atenção de segurança (score {risk}/100)")

        if not parts:
            return "É um script simples, com poucas estruturas avançadas."

        return "No geral, o código " + ", ".join(parts) + "."
