"""Relatório M1. Só declara execução verificada com os registros exigidos."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'evidence'
OUT = ROOT / 'deliverables'
W, H = 595.28, 841.89
GREEN = colors.HexColor('#254D3B')
INK = colors.HexColor('#24352D')
MUTED = colors.HexColor('#58695F')
LIGHT = colors.HexColor('#EDF3EE')
AMBER = colors.HexColor('#805400')
FONT = 'Helvetica'
BOLD = 'Helvetica-Bold'


def clean(text):
    return re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text).replace('\r', '\n')


def log_tail(name, count=6):
    p = EVIDENCE / name
    if not p.exists():
        return 'Não executado neste ambiente.'
    lines = [line for line in clean(p.read_text(errors='replace')).splitlines() if line.strip()]
    return '\n'.join(lines[-count:])


def local_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return 'Sem commit local identificado'


class Report:
    def __init__(self, verified):
        global FONT, BOLD
        regular = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
        bold = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
        if regular.exists() and bold.exists():
            pdfmetrics.registerFont(TTFont('ReportSans', str(regular)))
            pdfmetrics.registerFont(TTFont('ReportBold', str(bold)))
            FONT, BOLD = 'ReportSans', 'ReportBold'
        self.verified = verified
        self.name = os.getenv('STUDENT_NAME', 'Adalbert Raczkovi Junior')
        self.student_id = os.getenv('STUDENT_ID', '0015660')
        self.sha = os.getenv('GITHUB_SHA', local_hash())
        self.repo = os.getenv('GITHUB_REPOSITORY', 'Adalbert-junior/Minha_Biblioteca_GitHub')
        self.url = 'https://github.com/' + self.repo
        self.run_url = self.url + '/actions/runs/' + os.getenv('GITHUB_RUN_ID', '')
        self.versions = {}
        if (EVIDENCE / 'versions.json').exists():
            self.versions = json.loads((EVIDENCE / 'versions.json').read_text())
        OUT.mkdir(exist_ok=True)
        self.path = OUT / f'M1_trabalho_final_{self.student_id}_Adalbert_Raczkovi_Junior.pdf'
        self.c = canvas.Canvas(str(self.path), pagesize=(W, H))
        self.c.setTitle('Minha Biblioteca - Desenvolvimento Mobile I')
        self.c.setAuthor(self.name)
        self.c.setSubject('Relatório técnico com matriz dos 13 critérios')
        self.page_no = 0

    def page(self, title, subtitle='Desenvolvimento Mobile I | Unilavras | 2026/2'):
        if self.page_no:
            self.c.showPage()
        self.page_no += 1
        self.c.setFillColor(GREEN)
        self.c.rect(0, H-94, W, 94, stroke=0, fill=1)
        self.c.setFillColor(colors.white)
        self.c.setFont(BOLD, 19)
        self.c.drawString(40, H-45, title)
        self.c.setFont(FONT, 9)
        self.c.drawString(40, H-67, subtitle)
        self.c.setStrokeColor(colors.HexColor('#CCD8CE'))
        self.c.line(40, 42, W-40, 42)
        self.c.setFillColor(MUTED)
        self.c.setFont(FONT, 8)
        self.c.drawString(40, 27, f'Minha Biblioteca | {self.student_id}')
        self.c.drawRightString(W-40, 27, f'{self.page_no}/8')
        return H-116

    def para(self, text, y, x=40, width=W-80, size=10, leading=15, color=INK):
        style = ParagraphStyle('body', fontName=FONT, fontSize=size, leading=leading,
                               textColor=color, spaceAfter=0)
        p = Paragraph(text, style)
        _, height = p.wrap(width, H)
        if y-height < 54:
            raise ValueError(f'Texto excede página {self.page_no}: {text[:60]}')
        p.drawOn(self.c, x, y-height)
        return y-height-11

    def heading(self, text, y):
        self.c.setFillColor(GREEN)
        self.c.setFont(BOLD, 12)
        self.c.drawString(40, y-12, text)
        return y-30

    def code(self, text, y, height=None):
        lines = []
        for line in text.splitlines():
            lines.extend(textwrap.wrap(line, width=88, replace_whitespace=False,
                                       drop_whitespace=False) or [''])
        if height is None:
            height = 17 + 12*len(lines)
        if y-height < 54:
            raise ValueError(f'Código excede página {self.page_no}')
        self.c.setFillColor(LIGHT)
        self.c.roundRect(40, y-height, W-80, height, 7, fill=1, stroke=0)
        self.c.setFillColor(INK)
        self.c.setFont('Courier', 8.5)
        for i, line in enumerate(lines):
            self.c.drawString(50, y-17-i*12, line)
        return y-height-16

    def table(self, rows, widths, y, font_size=8.3):
        style = ParagraphStyle('cell', fontName=FONT, fontSize=font_size,
                               leading=font_size+3, textColor=INK)
        content = [[Paragraph(escape(str(cell)), style) for cell in row] for row in rows]
        t = Table(content, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D7E7DA')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, 0), .6, GREEN),
        ]))
        _, height = t.wrap(W-80, H)
        if y-height < 54:
            raise ValueError(f'Tabela excede página {self.page_no}, altura {height}')
        t.drawOn(self.c, 40, y-height)
        return y-height-15

    def image(self, name, x, top, width, height):
        p = EVIDENCE / (name+'.png')
        if not self.verified or not p.exists():
            raise ValueError('Captura real ausente: '+name)
        self.c.drawImage(str(p), x, top-height, width=width, height=height,
                         preserveAspectRatio=True, anchor='n', mask='auto')
        self.c.setStrokeColor(colors.HexColor('#C5D2C7'))
        self.c.rect(x, top-height, width, height, stroke=1, fill=0)

    def two_images(self, first, second, y, caption1, caption2):
        self.image(first, 53, y, 218, 472)
        self.image(second, 324, y, 218, 472)
        self.para(caption1, y-485, x=53, width=218, size=9, leading=13)
        self.para(caption2, y-485, x=324, width=218, size=9, leading=13)
        return y-551

    def run(self):
        self.cover()
        self.matrix()
        self.visual_a()
        self.visual_b()
        self.visual_c()
        self.responsive()
        self.quality()
        self.decisions()
        self.c.save()
        print(str(self.path))

    def cover(self):
        y = self.page('Minha Biblioteca', 'Relatório do trabalho final - catálogo pessoal local em Flutter')
        y = self.para('<b>'+escape(self.name)+'</b>', y-15, size=18, leading=25)
        y = self.para(f'Matrícula: <b>{escape(self.student_id)}</b><br/>'
                      'Curso: Análise e Desenvolvimento de Sistemas<br/>'
                      'Disciplina: Desenvolvimento Mobile I<br/>Turma: 2º semestre de 2026', y, size=11, leading=19)
        status = ('Verificações automatizadas concluídas na execução identificada.' if self.verified else
                  'Versão implementada; evidências de execução, testes e APK ainda pendentes.')
        y = self.para('<b>Situação:</b> '+status, y-10, color=GREEN if self.verified else AMBER)
        y = self.heading('1. Identificação e resumo', y-15)
        y = self.para('<b>Domínio e problema.</b> Um leitor precisa registrar quais livros pretende ler, '
                      'quais está lendo e quais concluiu. A Minha Biblioteca reúne título, autoria, '
                      'situação de leitura e notas em um catálogo simples, sem cadastro de usuário.', y)
        y = self.para('<b>Fluxo principal.</b> O aplicativo começa vazio. A ação de adicionar abre o '
                      'formulário; um envio válido inclui o livro e mostra confirmação. Tocar no cartão '
                      'abre o detalhe. A edição reutiliza o formulário, preserva o identificador e retorna '
                      'à coleção atualizada. Cancelar retorna sem alterar os dados.', y)
        y = self.para('<b>Escopo.</b> Três telas, coleção dinâmica em memória, estado vazio, validação, '
                      'criação, edição, componentes separados e tema Material 3. A coleção se perde '
                      'quando o processo é encerrado. Persistência, autenticação e serviços remotos '
                      'ficam fora desta versão.', y)
        if self.verified:
            text = ('As imagens das páginas 3 a 6 foram produzidas pelo motor Flutter em testes de '
                    'widgets. A abertura do APK foi verificada separadamente no emulador Android 10 '
                    '(API 29). A instalação e abertura não representam um teste manual de todos os fluxos.')
        else:
            text = ('Este documento não atribui aprovação a testes que não foram executados. As '
                    'páginas funcionais mostram a implementação e os cenários de verificação; não '
                    'substituem capturas de execução. O projeto inclui geração automática do PDF com '
                    'evidências reais após uma execução bem-sucedida no GitHub.')
        self.para(text, y-10, size=9, leading=14)

    def matrix(self):
        y = self.page('Versão e requisitos')
        y = self.heading('2. Repositório, versão e execução', y)
        repo_label = 'Repositório' if self.verified else 'Repositório de destino (nova versão não publicada)'
        y = self.para(f'<b>{repo_label}:</b><br/><link href="{escape(self.url)}">{escape(self.url)}</link><br/>'
                      f'<b>Hash:</b> {escape(self.sha)}', y, size=8.7, leading=13)
        version = (f"Flutter {self.versions.get('frameworkVersion', '?')}; Dart "
                   f"{self.versions.get('dartSdkVersion', '?')}" if self.verified else
                   'Ambiente previsto: Flutter 3.35.5 / Dart 3.9.2 / Java 17. Não houve execução Flutter válida.')
        y = self.para(version, y, size=8.7, leading=13)
        y = self.code('git clone '+self.url+'\ncd Minha_Biblioteca_GitHub\n'
                      'git checkout '+self.sha+'\nflutter pub get\nflutter analyze\n'
                      'flutter test --concurrency=1\nflutter run\nflutter build apk --release', y)
        if not self.verified:
            y = self.para('O checkout do hash acima só será reproduzível após sua publicação. '
                          'O workflow usa o hash do GitHub, e não este identificador local.', y, size=8, leading=11, color=AMBER)
        y = self.heading('3. Matriz dos 13 critérios', y)
        rows = [['Nº', 'Requisito', 'Evidência / localização']]
        entries = [
            ('1', 'Identificação, objetivo e fluxo', 'p. 1; este relatório'),
            ('2', 'Repositório, versão e execução', 'p. 2; README.md; publicação '+('verificada' if self.verified else 'pendente')),
            ('3', 'Execução e artefato Android', 'p. 7; build e emulador '+('concluídos' if self.verified else 'pendentes')),
            ('4', 'Telas e navegação', 'pp. 3-5; lib/pages/'),
            ('5', 'Coleção e estado vazio', 'p. 3; catalog_page.dart; empty_catalog.dart'),
            ('6', 'Detalhe selecionado', 'p. 4; book_detail_page.dart'),
            ('7', 'Formulário e validação', 'p. 4; book_form_page.dart'),
            ('8', 'Criação e edição local', 'p. 5; catalog_page.dart; catalog_test.dart'),
            ('9', 'Modelo e widgets organizados', 'p. 7; models/; widgets/'),
            ('10', 'Dois espaços sem overflow', 'p. 6; testes 390/840 px '+('aprovados' if self.verified else 'não executados')),
            ('11', 'Tema e acessibilidade', 'p. 6; app_theme.dart; testes de diretrizes'),
            ('12', 'Análise e teste de widget', 'p. 7; test/; '+('execução concluída' if self.verified else 'testes pendentes')),
            ('13', 'Decisões, fontes e autoria', 'p. 8; este relatório; README.md'),
        ]
        rows += entries
        self.table(rows, [25, 184, W-80-209], y, font_size=7.5)

    def pending_visual(self, y, description, steps, source, expected):
        y = self.para('<b>Evidência de execução pendente.</b> '+description, y, color=AMBER)
        y = self.heading('Cenário reproduzível', y-8)
        for i, step in enumerate(steps, 1):
            y = self.para(f'<b>{i}.</b> '+step, y)
        y = self.heading('Trecho implementado', y-8)
        y = self.code(source, y)
        y = self.heading('Resultado esperado e teste correspondente', y-8)
        self.para(expected, y)

    def visual_a(self):
        y = self.page('Coleção e estado vazio', '4. Evidências visuais e funcionais - A e B')
        if self.verified:
            y = self.two_images('01_vazio', '07_lista_390', y,
                '<b>A.</b> Aplicativo montado sem livros. Há mensagem e ação nomeada.',
                '<b>B.</b> Dois objetos de teste exibidos a partir da coleção dinâmica.')
            self.para('Capturas reais de testes de widgets em 390 pixels lógicos. '
                      'Os livros da imagem B são dados de teste; o aplicativo instalado inicia vazio.', y, size=9)
        else:
            self.pending_visual(y,
                'O código contém os dois estados. Não há captura de um aplicativo executado neste ambiente.',
                ['Abrir o aplicativo sem itens e conferir a mensagem de vazio.',
                 'Tocar em “Adicionar primeiro livro”, informar título e autoria e salvar.',
                 'Conferir a confirmação e o cartão; adicionar um segundo livro.'],
                "_books.isEmpty\n  ? EmptyCatalog(onAdd: _add)\n  : Wrap(children: _books.map((book) =>\n      BookCard(book: book, onTap: () => _detail(book))\n    ).toList());",
                'O teste “coleção vazia tem mensagem e ação útil” exige uma mensagem e nenhum '
                'BookCard. O teste de criação exige exatamente um cartão após o envio. '
                'Arquivos: catalog_page.dart, empty_catalog.dart e catalog_test.dart. '
                'Esses testes foram escritos, mas sua aprovação ainda não foi observada.')

    def visual_b(self):
        y = self.page('Detalhe e validação', '4. Evidências visuais e funcionais - C, D e E')
        if self.verified:
            y = self.two_images('04_detalhe', '02_validacao', y,
                '<b>C/D.</b> Dom Casmurro selecionado; título, autoria, situação e notas correspondem ao item.',
                '<b>E.</b> Envio vazio rejeitado. As mensagens indicam os campos obrigatórios.')
            self.para('O formulário permanece aberto diante de entrada inválida. A validação considera '
                      'texto com apenas espaços inválido. Não há inclusão antes de FormState.validate().', y, size=9)
        else:
            self.pending_visual(y,
                'Navegação e validação estão implementadas; faltam capturas reais desses fluxos.',
                ['Criar Dom Casmurro, autoria Machado de Assis, com uma nota opcional.',
                 'Abrir o cartão e conferir os dados na página de detalhes.',
                 'Abrir um novo cadastro, informar apenas espaços no título e salvar sem autoria.'],
                "validator: (v) => (v ?? '').trim().isEmpty\n    ? 'Informe o título' : null;\n\nif (!_formKey.currentState!.validate()) return;\nNavigator.pop(context, Book(...));",
                'O teste de formulário exige “Informe o título” e “Informe a autoria”, sem sair '
                'da página. O teste do detalhe exige “Autoria: Machado de Assis”. Cancelar o '
                'cadastro inválido deve manter a coleção vazia. Local: book_form_page.dart, '
                'book_detail_page.dart e catalog_test.dart.')

    def visual_c(self):
        y = self.page('Criação e edição', '4. Evidências visuais e funcionais - F')
        if self.verified:
            y = self.two_images('03_criacao', '06_edicao', y,
                '<b>Antes.</b> Cadastro válido de Dom Casmurro, na situação Quero ler.',
                '<b>Depois.</b> Edição para Lido. Permanece um único cartão; a confirmação mostra a atualização.')
            self.para('As duas imagens pertencem ao mesmo fluxo executado por evidence_test.dart. '
                      'O teste catalog_test.dart verifica também que editar títulos iguais usa a identidade '
                      'do objeto e não altera o outro livro.', y, size=9)
        else:
            self.pending_visual(y,
                'A edição preserva id e substitui o item correspondente; falta comprovação em execução.',
                ['Salvar um livro e conferir “Livro cadastrado”.',
                 'Abrir o detalhe, tocar em “Editar livro” e mudar a situação para Lido.',
                 'Salvar e conferir “Livro atualizado”, mantendo apenas um cartão.'],
                'final index = _books.indexWhere((b) => b.id == book.id);\n'
                'setState(() {\n  if (index < 0) {\n    _books.add(book); _nextId++;\n'
                '  } else {\n    _books[index] = book;\n  }\n});',
                'O teste de criação/detalhe/edição verifica um BookCard antes e depois da edição, '
                'o novo título e a situação Lido. Um segundo teste inicia dois livros com o mesmo '
                'título e garante que só o segundo muda. Local: catalog_page.dart e catalog_test.dart.')

    def responsive(self):
        y = self.page('Layout e acessibilidade', '4. Evidências visuais e funcionais - G')
        if self.verified:
            self.image('07_lista_390', 45, y, 155, 355)
            self.image('07_lista_840', 220, y, 330, 355)
            y = self.para('Mesmo conteúdo em <b>390 × 900</b> e <b>840 × 900</b> pixels lógicos. '
                          'À esquerda, uma coluna; à direita, duas. Os testes percorrem lista, detalhe '
                          'e formulário nas duas larguras, com escala de texto 1,0 e 2,0.', y-370, size=9)
        else:
            y = self.para('<b>Capturas e verificação sem overflow pendentes.</b> Foram escritos cenários '
                          'para 390 × 844 e 840 × 900 pixels lógicos, com fonte a 100% e 200%. '
                          'Não se declara ausência de overflow antes de executar os testes.', y, color=AMBER)
            y = self.code('final wide = constraints.maxWidth >= 700;\n'
                          'final width = (constraints.maxWidth - 32 -\n'
                          '    (wide ? 16 : 0)) / (wide ? 2 : 1);\n'
                          'Wrap(spacing: 16, runSpacing: 12, children: ...);', y)
        y = self.heading('Adaptação', y)
        y = self.para('LayoutBuilder decide o número de colunas em 700 pixels. A coleção utiliza '
                      'Wrap e cartões sem altura fixa. Formulário e detalhe possuem rolagem, margem '
                      'de 24 pixels e largura máxima de 640 pixels. SafeArea protege o conteúdo '
                      'de recortes do sistema. Títulos longos são resumidos no cartão e exibidos '
                      'completos no detalhe.', y, size=9, leading=14)
        y = self.heading('Tema e acessibilidade', y)
        self.para('O tema usa Material 3 e ColorScheme.fromSeed. Campos possuem rótulos persistentes; '
                  'ações importantes combinam texto e ícone. O cartão oferece rótulo semântico com '
                  'título, autoria e situação. A ordem dos campos acompanha a leitura. Há testes '
                  'para rótulos, alvos de toque Android e contraste nas telas de coleção. '
                  + ('Essas diretrizes passaram no ambiente de testes; não houve avaliação com leitor '
                     'de tela por uma pessoa.' if self.verified else 'As diretrizes ainda precisam ser executadas.'),
                  y, size=9, leading=14)

    def quality(self):
        y = self.page('Organização e qualidade')
        y = self.heading('5. Organização e qualidade', y)
        y = self.para('Book separa identidade e dados do domínio. CatalogPage é proprietária da coleção '
                      'em memória. BookDetailPage consulta um item; BookFormPage concentra os '
                      'validadores e a edição. BookCard organiza a apresentação de cada livro e '
                      'EmptyCatalog concentra a orientação inicial. O tema está em theme/app_theme.dart.', y, size=9)
        y = self.para('<b>Componentização.</b> BookCard foi extraído porque cada item precisa da mesma '
                      'apresentação e semântica. CatalogPage decide quais objetos exibir e como '
                      'atualizá-los, sem repetir a composição do cartão.', y, size=9)
        y = self.heading('Análise, testes e build - registros da versão', y)
        if self.verified:
            for title, name, count in [('Formatação e análise', 'analyze.txt', 3),
                                        ('Suíte completa de testes', 'test.txt', 4),
                                        ('Build Android', 'build.txt', 4),
                                        ('Instalação e abertura no Android API 29', 'android.txt', 5)]:
                y = self.para('<b>'+title+'</b>', y, size=9, leading=12)
                y = self.code(log_tail(name, count), y)
            p = OUT/'app-release.apk'
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            y = self.para('APK: app-release.apk, '+f'{p.stat().st_size/1048576:.1f} MiB.'
                          '<br/>SHA-256: '+digest, y, size=7.2, leading=11)
        else:
            y = self.para('Foi possível executar o formatador e o analisador Dart diretamente, com '
                          'arquivos e dependências locais. Esse procedimento não equivale a executar '
                          'flutter analyze, flutter test ou flutter build apk.', y, size=9)
            y = self.code('dart format lib test\n'+log_tail('offline-analyze.txt', 4), y)
            y = self.table([
                ['Verificação exigida', 'Situação local'],
                ['flutter analyze', 'Pendente; análise Dart alternativa sem problemas.'],
                ['flutter test', 'Suíte escrita; execução não realizada.'],
                ['flutter build apk', 'Pendente; nenhum APK gerado.'],
                ['Instalação / abertura Android', 'Pendente; nenhum emulador executado.'],
            ], [184, W-80-184], y, font_size=9)
            y = self.para('A revisão automática bloqueou a execução Flutter por tentativa de acesso '
                          'ao serviço de metadados da máquina, uma fronteira sensível a credenciais. '
                          'O bloqueio não é apresentado como resultado de teste do aplicativo.', y, size=9, color=AMBER)
        self.para('Os testes relevantes protegem vazio, validação, cancelamento, criação, edição e '
                  'identidade. Os logs completos e PNGs gerados ficam no artifact da execução. '
                  + (f'<link href="{escape(self.run_url)}">Registro da execução no GitHub Actions</link>.'
                     if self.verified else 'A execução automática ainda precisa ser iniciada no repositório publicado.'),
                  y, size=8.5, leading=13)

    def decisions(self):
        y = self.page('Decisões, fontes e contribuição')
        y = self.heading('6. Decisões, dificuldade, fontes e autoria', y)
        y = self.para('<b>Decisão técnica.</b> O catálogo usa setState e List&lt;Book&gt; porque o '
                      'escopo é pequeno e local. Um único formulário atende criação e edição. '
                      'O id direciona a substituição; título não funciona como chave, pois duas '
                      'obras podem ter o mesmo nome. Controllers são liberados em dispose().', y)
        y = self.para('<b>Dificuldade e solução.</b> A conferência do repositório de destino encontrou '
                      'arquivos soltos na raiz, sem a organização esperada pelo Flutter. O pacote '
                      'organiza lib/, android/, test/, tools/ e o workflow. A execução local Flutter '
                      'foi bloqueada; a solução documental foi registrar a limitação e preparar '
                      'uma rotina reproduzível que reúne evidências do mesmo commit.', y)
        y = self.para('<b>Rastreabilidade.</b> O workflow interrompe diante de erro. O modo verificado '
                      'do gerador exige marcadores de sucesso para análise, testes, build e abertura '
                      'Android, os registros e as imagens do fluxo. O PDF usa GITHUB_SHA e a URL '
                      'do repositório que executou a rotina. Caches, APKs e capturas não são '
                      'versionados; são disponibilizados como artifacts.', y)
        y = self.heading('Fontes e recursos externos', y)
        sources = [
            ('Formulários e validação', 'https://docs.flutter.dev/cookbook/forms/validation'),
            ('Testes de widgets', 'https://docs.flutter.dev/cookbook/testing/widget/introduction'),
            ('Layout adaptativo', 'https://docs.flutter.dev/ui/adaptive-responsive'),
            ('Acessibilidade', 'https://docs.flutter.dev/ui/accessibility'),
        ]
        for title, url in sources:
            y = self.para(f'{title}: <link href="{url}">{url}</link>', y, size=8, leading=12)
        y = self.para('Consultadas em 05/10/2026 (UTC). Templates Android e ícones Material do '
                      'Flutter SDK 3.35.5; Gradle Wrapper 8.12. ReportLab gera o PDF. DejaVu Sans '
                      'é usada nas capturas do ambiente de testes Linux para evitar a fonte Ahem. '
                      'Essas dependências documentais não são bibliotecas do aplicativo.', y, size=8.5, leading=13)
        y = self.heading('Responsabilidade e contribuição externa', y)
        y = self.para('Responsável pela entrega: '+escape(self.name)+'. Programação, testes e '
                      'redação foram preparados com assistência do ChatGPT. Este relatório '
                      'distingue código escrito de evidência efetivamente executada. A revisão '
                      'pessoal, a conferência das regras da disciplina e o envio cabem ao estudante; '
                      'não se afirma que essa revisão já ocorreu.', y, size=9, leading=14)
        if not self.verified:
            self.para('<b>Antes da entrega:</b> publicar o conteúdo do ZIP preservando as pastas, '
                      'aguardar o workflow concluir, baixar M1-entrega-0015660, conferir o PDF '
                      'verificado e enviar somente esse PDF. Esta versão local ainda contém '
                      'pendências e não comprova os 13 pontos integralmente.', y, size=9, leading=14, color=AMBER)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verified', action='store_true')
    args = parser.parse_args()
    if args.verified:
        required = ['analyze.ok', 'test.ok', 'build.ok', 'android.ok', 'versions.json',
                    'analyze.txt', 'test.txt', 'build.txt', 'android.txt']
        required += [x+'.png' for x in ['01_vazio', '02_validacao', '03_criacao',
                    '04_detalhe', '05_editar', '06_edicao', '07_lista_390', '07_lista_840']]
        missing = [f for f in required if not (EVIDENCE/f).is_file()]
        if not (OUT/'app-release.apk').is_file():
            missing.append('app-release.apk')
        if not os.getenv('GITHUB_SHA') or not os.getenv('GITHUB_REPOSITORY'):
            missing.append('identificação da execução GitHub')
        if missing:
            raise SystemExit('Não é possível declarar verificação concluída: '+', '.join(missing))
    Report(args.verified).run()


if __name__ == '__main__':
    main()
