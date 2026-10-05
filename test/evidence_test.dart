import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:minha_biblioteca/main.dart';
import 'package:minha_biblioteca/widgets/book_card.dart';
import 'catalog_test.dart' show examples, save, press, enter;

const boundaryKey = Key('captureBoundary');

Future<void> capture(WidgetTester tester, String name) async {
  await tester.pumpAndSettle();
  expect(tester.takeException(), isNull);
  final boundary = tester.renderObject<RenderRepaintBoundary>(
    find.byKey(boundaryKey),
  );
  await tester.runAsync(() async {
    final image = await boundary.toImage(pixelRatio: 1.5);
    final data = await image.toByteData(format: ui.ImageByteFormat.png);
    final file = File('evidence/$name.png');
    await file.parent.create(recursive: true);
    await file.writeAsBytes(data!.buffer.asUint8List());
    image.dispose();
  });
}

void main() {
  setUpAll(() async {
    final fontFile = File('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf');
    if (fontFile.existsSync()) {
      final loader = FontLoader('Roboto');
      loader.addFont(
        Future.value(ByteData.sublistView(await fontFile.readAsBytes())),
      );
      await loader.load();
    }
  });

  testWidgets(
    'captura o fluxo real de vazio, validação, criação, detalhe e edição',
    (tester) async {
      tester.view.devicePixelRatio = 1;
      tester.view.physicalSize = const Size(390, 844);
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        const RepaintBoundary(key: boundaryKey, child: LibraryApp()),
      );
      await capture(tester, '01_vazio');
      await press(tester, find.text('Adicionar primeiro livro'));
      await tester.pumpAndSettle();
      await save(tester);
      expect(find.text('Informe o título'), findsOneWidget);
      expect(find.text('Informe a autoria'), findsOneWidget);
      await tester.drag(
        find.byType(SingleChildScrollView).first,
        const Offset(0, 500),
      );
      await tester.pumpAndSettle();
      await capture(tester, '02_validacao');
      await enter(tester, 'titleField', 'Dom Casmurro');
      await enter(tester, 'authorField', 'Machado de Assis');
      await enter(tester, 'notesField', 'Leitura para as férias.');
      await save(tester);
      expect(find.byType(BookCard), findsOneWidget);
      await capture(tester, '03_criacao');
      await press(tester, find.text('Dom Casmurro'));
      await tester.pumpAndSettle();
      expect(find.text('Autoria: Machado de Assis'), findsOneWidget);
      await capture(tester, '04_detalhe');
      await press(tester, find.text('Editar livro'));
      await tester.pumpAndSettle();
      await capture(tester, '05_editar');
      await press(tester, find.byKey(const Key('statusField')));
      await tester.pumpAndSettle();
      await press(tester, find.text('Lido').last);
      await tester.pumpAndSettle();
      await save(tester);
      expect(find.byType(BookCard), findsOneWidget);
      expect(find.text('Lido'), findsOneWidget);
      await capture(tester, '06_edicao');
    },
  );

  for (final width in [390.0, 840.0]) {
    testWidgets('captura coleção comparável com largura $width', (
      tester,
    ) async {
      tester.view.devicePixelRatio = 1;
      tester.view.physicalSize = Size(width, 900);
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        const RepaintBoundary(
          key: boundaryKey,
          child: LibraryApp(initialBooks: examples),
        ),
      );
      await capture(tester, '07_lista_${width.toInt()}');
      expect(find.byType(BookCard), findsNWidgets(2));
    });
  }
}
