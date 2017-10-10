import scala.util.matching.Regex
import scala.io.Source
import java.io.File
import java.io.PrintWriter

object Extractor {
  def main(args: Array[String]): Unit = {
    val urlFile = new File("/Users/christophorus/Desktop/Proxy-Hentai-Downloader/urls.txt")
    val urlPrintWriter = new PrintWriter(urlFile)
    val documentName = "view-source_https___exhentai.org_favorites.php.html"
    println(s"Now parsing document $documentName")
    val resultUrlString = parse(documentName)
    urlPrintWriter.write(" " + resultUrlString)
    println(s"Document $documentName has been parsed!")
    urlPrintWriter.close()
  }

  val parse = (documentName: String) => {
    val pattern = new Regex("https://exhentai.org/g/[0-9]+/[0-9a-z]{10}/")
    val bufferSource = Source.fromFile("/Users/christophorus/Downloads/php/" + documentName)
    val fileString = bufferSource.getLines().mkString
    bufferSource.close
    val urlList = pattern.findAllIn(fileString).toList
    val cleanList = for {(url, count) <- urlList.zipWithIndex if count % 2 == 0} yield url
    cleanList.mkString(" ")
  }
}
