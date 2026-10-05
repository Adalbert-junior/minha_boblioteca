enum ReadingStatus { planned, reading, finished }

extension ReadingStatusLabel on ReadingStatus {
  String get label => switch (this) {
    ReadingStatus.planned => 'Quero ler',
    ReadingStatus.reading => 'Lendo',
    ReadingStatus.finished => 'Lido',
  };
}

class Book {
  const Book({
    required this.id,
    required this.title,
    required this.author,
    required this.status,
    this.notes = '',
  });
  final int id;
  final String title;
  final String author;
  final ReadingStatus status;
  final String notes;
}
