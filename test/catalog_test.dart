import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:minha_biblioteca/main.dart';
import 'package:minha_biblioteca/models/book.dart';
import 'package:minha_biblioteca/widgets/book_card.dart';

const examples = [
  Book(
    id: 1,
    title: 'Dom Casmurro',
    author: 'Machado de Assis',
    status: ReadingStatus.planned,
  ),
  Book(
    id: 2,
    title: 'A hora da estrela',
    author: 'Clarice Lispector',
    status: ReadingStatus.reading,
  ),
];

Future<void> save(WidgetTester tester) async {
  await tester.ensureVisible(find.byKey(const Key('saveButton')));
  await tester.tap(find.byKey(const Key('saveButton')));
  await tester.pumpAndSettle();
}

void main() {
  testWidgets('ações visíveis têm rótulos e áreas mínimas de toque', (
    tester,
  ) async {
    final handle = tester.ensureSemantics();
    addTearDown(handle.dispose);
    await tester.pumpWidget(const LibraryApp());
    await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));
    await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
    await expectLater(tester, meetsGuideline(textContrastGuideline));
    await tester.pumpWidget(const LibraryApp(initialBooks: examples));
    await tester.pumpAndSettle();
    await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));
    await expectLater(tester, meetsGuideline(androidTapTargetGuideline));
    await expectLater(tester, meetsGuideline(textContrastGuideline));
  });

  testWidgets('coleção vazia tem mensagem e ação útil', (tester) async {
    await tester.pumpWidget(const LibraryApp());
    expect(find.text('Nenhum livro cadastrado'), findsOneWidget);
    expect(find.byType(BookCard), findsNothing);
    await tester.tap(find.text('Adicionar primeiro livro'));
    await tester.pumpAndSettle();
    expect(find.text('Novo livro'), findsOneWidget);
  });

  testWidgets('campos em branco não criam livro; cancelar preserva vazio', (
    tester,
  ) async {
    await tester.pumpWidget(const LibraryApp());
    await tester.tap(find.text('Adicionar primeiro livro'));
    await tester.pumpAndSettle();
    await tester.enterText(find.byKey(const Key('titleField')), '   ');
    await save(tester);
    expect(find.text('Informe o título'), findsOneWidget);
    expect(find.text('Informe a autoria'), findsOneWidget);
    expect(find.text('Novo livro'), findsOneWidget);
    await tester.ensureVisible(find.text('Cancelar'));
    await tester.tap(find.text('Cancelar'));
    await tester.pumpAndSettle();
    expect(find.text('Nenhum livro cadastrado'), findsOneWidget);
  });

  testWidgets('criação, detalhe e edição refletem o mesmo item', (
    tester,
  ) async {
    await tester.pumpWidget(const LibraryApp());
    await tester.tap(find.text('Adicionar primeiro livro'));
    await tester.pumpAndSettle();
    await tester.enterText(
      find.byKey(const Key('titleField')),
      '  Dom Casmurro  ',
    );
    await tester.enterText(
      find.byKey(const Key('authorField')),
      'Machado de Assis',
    );
    await save(tester);
    expect(find.byType(BookCard), findsOneWidget);
    expect(find.text('Livro cadastrado'), findsOneWidget);
    await tester.tap(find.text('Dom Casmurro'));
    await tester.pumpAndSettle();
    expect(find.text('Autoria: Machado de Assis'), findsOneWidget);
    await tester.tap(find.text('Editar livro'));
    await tester.pumpAndSettle();
    await tester.enterText(
      find.byKey(const Key('titleField')),
      'Dom Casmurro - relido',
    );
    await tester.tap(find.byKey(const Key('statusField')));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Lido').last);
    await tester.pumpAndSettle();
    await save(tester);
    expect(find.byType(BookCard), findsOneWidget);
    expect(find.text('Dom Casmurro - relido'), findsOneWidget);
    expect(find.text('Lido'), findsOneWidget);
    expect(find.text('Livro atualizado'), findsOneWidget);
  });

  testWidgets('editar um título duplicado não muda o outro objeto', (
    tester,
  ) async {
    await tester.pumpWidget(
      const LibraryApp(
        initialBooks: [
          Book(
            id: 1,
            title: 'Mesmo título',
            author: 'Autoria A',
            status: ReadingStatus.planned,
          ),
          Book(
            id: 2,
            title: 'Mesmo título',
            author: 'Autoria B',
            status: ReadingStatus.reading,
          ),
        ],
      ),
    );
    await tester.tap(find.byType(BookCard).last);
    await tester.pumpAndSettle();
    await tester.tap(find.text('Editar livro'));
    await tester.pumpAndSettle();
    await tester.enterText(
      find.byKey(const Key('titleField')),
      'Segundo livro editado',
    );
    await save(tester);
    expect(find.text('Mesmo título'), findsOneWidget);
    expect(find.text('Segundo livro editado'), findsOneWidget);
    expect(find.text('Autoria A'), findsOneWidget);
    expect(find.byType(BookCard), findsNWidgets(2));
  });

  for (final size in [const Size(390, 844), const Size(840, 900)]) {
    for (final scale in [1.0, 2.0]) {
      testWidgets(
        'lista, detalhe e formulário sem exceção em $size, escala $scale',
        (tester) async {
          tester.view.devicePixelRatio = 1;
          tester.view.physicalSize = size;
          addTearDown(tester.view.resetPhysicalSize);
          addTearDown(tester.view.resetDevicePixelRatio);
          tester.platformDispatcher.textScaleFactorTestValue = scale;
          addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);
          await tester.pumpWidget(const LibraryApp(initialBooks: examples));
          await tester.pumpAndSettle();
          expect(tester.takeException(), isNull);
          await tester.tap(find.text('Dom Casmurro'));
          await tester.pumpAndSettle();
          expect(tester.takeException(), isNull);
          await tester.ensureVisible(find.text('Editar livro'));
          await tester.tap(find.text('Editar livro'));
          await tester.pumpAndSettle();
          expect(tester.takeException(), isNull);
          await save(tester);
          expect(tester.takeException(), isNull);
        },
      );
    }
  }
}
