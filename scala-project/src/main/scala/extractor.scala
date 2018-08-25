import scala.collection.mutable.ListBuffer
import scala.util.matching.Regex
import scala.io.Source
import java.io.File
import java.io.PrintWriter
import java.nio.file.{Paths, Files}

object Extractor {
  def main(args: Array[String]): Unit = {
    val urlFile = new File(
      "/Users/christophorus/Desktop/Proxy-Hentai-Downloader/urls.txt")
    val urlPrintWriter = new PrintWriter(urlFile)
    val documentName =
      s"/Users/christophorus/Downloads/php/view-source_https___exhentai.org_favorites.php.html"
    val resultUrlStringList = new ListBuffer[String]()
    if (Files.exists(Paths.get(documentName))) {
      println(s"Now parsing document $documentName")
      resultUrlStringList ++= parse(documentName)
      println(s"Document $documentName has been parsed!")
    } else {
      println(s"$documentName does not exit.")
    }

    for (i <- 1 to 50) {
      val documentName =
        s"/Users/christophorus/Downloads/php/view-source_https___exhentai.org_favorites.php_page=$i.html"
      if (Files.exists(Paths.get(documentName))) {
        println(s"Now parsing document $documentName")
        resultUrlStringList ++= parse(documentName)
        println(s"Document $documentName has been parsed!")
      } else {
        println(s"$documentName does not exit.")
      }
    }

    urlPrintWriter.write(resultUrlStringList.mkString(" "))
    urlPrintWriter.close()
  }

  val parse = (documentName: String) => {
    val pattern = new Regex("https://exhentai.org/g/[0-9]+/[0-9a-z]{10}/")
    val bufferSource = Source.fromFile(documentName)
    val fileString = bufferSource.getLines().mkString
    bufferSource.close
    val urlList = pattern.findAllIn(fileString).toList
    val cleanList = for {
      (url, count) <- urlList.zipWithIndex if count % 2 == 0
    } yield url
    cleanList
  }
}
