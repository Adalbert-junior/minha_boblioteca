import 'package:flutter/material.dart';
import '../models/book.dart';
import '../widgets/book_card.dart';
import '../widgets/empty_catalog.dart';
import 'book_detail_page.dart';
import 'book_form_page.dart';

class CatalogPage extends StatefulWidget {
  const CatalogPage({super.key, this.initialBooks = const []});
  final List<Book> initialBooks;
  @override
  State<CatalogPage> createState() => _CatalogPageState();
}

class _CatalogPageState extends State<CatalogPage> {
  late final List<Book> _books = List.of(widget.initialBooks);
  late int _nextId = _books.fold<int>(0, (v, b) => b.id > v ? b.id : v) + 1;

  void _apply(Book book) {
    final index = _books.indexWhere((b) => b.id == book.id);
    setState(() {
      if (index < 0) {
        _books.add(book);
        _nextId++;
      } else {
        _books[index] = book;
      }
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(index < 0 ? 'Livro cadastrado' : 'Livro atualizado'),
      ),
    );
  }

  Future<void> _add() async {
    final book = await Navigator.push<Book>(
      context,
      MaterialPageRoute(builder: (_) => BookFormPage(newId: _nextId)),
    );
    if (mounted && book != null) _apply(book);
  }

  Future<void> _detail(Book book) async {
    final updated = await Navigator.push<Book>(
      context,
      MaterialPageRoute(builder: (_) => BookDetailPage(book: book)),
    );
    if (mounted && updated != null) _apply(updated);
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Minha Biblioteca')),
    floatingActionButton: _books.isEmpty
        ? null
        : FloatingActionButton.extended(
            tooltip: 'Cadastrar novo livro',
            onPressed: _add,
            icon: const Icon(Icons.add),
            label: const Text('Adicionar livro'),
          ),
    body: SafeArea(
      child: _books.isEmpty
          ? EmptyCatalog(onAdd: _add)
          : Align(
              alignment: Alignment.topCenter,
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 1000),
                child: LayoutBuilder(
                  builder: (context, constraints) {
                    final wide = constraints.maxWidth >= 700;
                    final width =
                        (constraints.maxWidth - 32 - (wide ? 16 : 0)) /
                        (wide ? 2 : 1);
                    return SingleChildScrollView(
                      padding: const EdgeInsets.fromLTRB(16, 16, 16, 100),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Padding(
                            padding: const EdgeInsets.only(left: 8, bottom: 16),
                            child: Text(
                              '${_books.length} livro(s) no catálogo',
                              style: Theme.of(context).textTheme.titleMedium,
                            ),
                          ),
                          Wrap(
                            spacing: 16,
                            runSpacing: 12,
                            children: _books
                                .map(
                                  (book) => SizedBox(
                                    width: width,
                                    child: BookCard(
                                      book: book,
                                      onTap: () => _detail(book),
                                    ),
                                  ),
                                )
                                .toList(),
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),
            ),
    ),
  );
}
