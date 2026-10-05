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
- todas funcionalidades ok e testadas

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

estrutura testada, funcionando e commitada

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


## Fontes e contribuições

- Flutter: https://docs.flutter.dev/cookbook/forms/validation
- Flutter: https://docs.flutter.dev/cookbook/testing/widget/introduction
- Flutter: https://docs.flutter.dev/ui/adaptive-responsive
- Flutter: https://docs.flutter.dev/ui/accessibility
- Templates Android e ícones Material fornecidos pelo Flutter SDK 3.35.5.
- Gradle Wrapper oficial 8.12.


