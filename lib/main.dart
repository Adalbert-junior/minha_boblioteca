import 'package:flutter/material.dart';
import 'models/book.dart';
import 'pages/catalog_page.dart';
import 'theme/app_theme.dart';

void main() => runApp(const LibraryApp());

class LibraryApp extends StatelessWidget {
  const LibraryApp({super.key, this.initialBooks = const []});
  final List<Book> initialBooks;

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Minha Biblioteca',
    debugShowCheckedModeBanner: false,
    theme: buildAppTheme(),
    home: CatalogPage(initialBooks: initialBooks),
  );
}
