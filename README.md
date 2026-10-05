# Minha Biblioteca

Catálogo pessoal de livros para Desenvolvimento Mobile I (Unilavras, 2026/2).
Responsável pela entrega: Adalbert Raczkovi Junior, matrícula 0015660.

## Funcionalidades

- Coleção inicialmente vazia, com ação para cadastrar o primeiro livro.
- Cadastro com título, autoria, situação (quero ler, lendo ou lido) e notas.
- Validação de campos obrigatórios, inclusive entradas com apenas espaços.
- Detalhe do livro selecionado e edição do mesmo objeto sem duplicação.
- Confirmação por SnackBar; cancelamento não altera a coleção.
- Material 3, rótulos, semântica e layout com uma ou duas colunas.

Os dados ficam na memória enquanto o aplicativo está aberto. Encerrar o processo
limpa a coleção. Não existem login, API ou banco de dados.

## Executar

Use Flutter **3.35.5**, Dart **3.9.2**, JDK **17** e Android SDK disponível.
Na pasta que contém este README e `pubspec.yaml`:

```sh
flutter pub get
dart format lib test
flutter analyze
flutter test --concurrency=1 --reporter expanded
flutter run
flutter build apk --release
```

O APK fica em `build/app/outputs/flutter-apk/app-release.apk`.
A assinatura de desenvolvimento serve para avaliação; publicar em loja exige
configurar uma chave própria. Não versione `local.properties` nem caches.

## Gerar a entrega sem instalar Flutter no seu computador

1. Extraia o ZIP. Abra a pasta `minha_biblioteca`.
2. Publique **o conteúdo dessa pasta**, preservando `lib/`, `android/`, `test/`,
   `tools/` e `.github/workflows/`. Não arraste todos os arquivos internos soltos.
   Prefira GitHub Desktop para incluir a pasta `.github` corretamente.
3. No repositório público, abra **Actions > M1 - verificar e gerar PDF**.
   O fluxo inicia quando há um push para `main` ou `master`; também pode ser
   iniciado pelo botão **Run workflow**.
4. Após todos os passos ficarem verdes, baixe **M1-entrega-0015660**, nos
   artifacts da execução. Ele contém o PDF com o hash real, APK e registros.
5. Abra o PDF, confira as capturas e o link do commit. Na disciplina, envie
   somente `M1_trabalho_final_0015660_Adalbert_Raczkovi_Junior.pdf`.

Se a execução falhar, o artifact `M1-diagnostico` traz as saídas disponíveis.
Não use resultados de um commit anterior para descrever uma versão nova.

## Estrutura

```text
lib/main.dart
lib/models/book.dart
lib/pages/catalog_page.dart
lib/pages/book_detail_page.dart
lib/pages/book_form_page.dart
lib/widgets/book_card.dart
lib/widgets/empty_catalog.dart
lib/theme/app_theme.dart
test/catalog_test.dart
test/evidence_test.dart
tools/report.py
.github/workflows/m1.yml
android/
```

`catalog_test.dart` testa vazio, validação, cancelamento, criação, detalhe,
edição, identidade de títulos duplicados, acessibilidade e telas de 390 e
840 pixels lógicos com texto a 100% e 200%.
`evidence_test.dart` produz PNGs da interface real renderizada pelo Flutter
durante os testes. Eles não são capturas de dispositivo; a captura Android
de abertura é gerada separadamente no emulador.

## Situação do pacote local

O código foi escrito, formatado e analisado por Dart diretamente, sem problemas
na análise local. Os comandos Flutter de teste e build não puderam ser
executados neste ambiente porque a revisão automática bloqueou um acesso ao
serviço de metadados da máquina. Portanto, este pacote não alega testes
aprovados nem APK já gerado. O PDF local registra essas pendências.
O workflow só gera a versão verificada do PDF após análise, testes, build e
abertura do APK terminarem com sucesso, com o hash do commit executado.

## Fontes e contribuições

- Flutter: https://docs.flutter.dev/cookbook/forms/validation
- Flutter: https://docs.flutter.dev/cookbook/testing/widget/introduction
- Flutter: https://docs.flutter.dev/ui/adaptive-responsive
- Flutter: https://docs.flutter.dev/ui/accessibility
- Templates Android e ícones Material fornecidos pelo Flutter SDK 3.35.5.
- Gradle Wrapper oficial 8.12.
- Programação, testes e redação com assistência do ChatGPT. A revisão pessoal
  e o envio são responsabilidade do estudante; não se presume revisão já feita.
- Nos PNGs dos testes em Linux, DejaVu Sans substitui a fonte de teste Ahem.

O relatório é gerado com ReportLab; essa dependência pertence apenas às
ferramentas documentais, não ao aplicativo Android.
