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
    val displayName =
      s"view-source_https___exhentai.org_favorites.php.html"
    val documentName = "/Users/christophorus/Downloads/php/" + displayName
    val resultUrlStringList = new ListBuffer[String]()
    if (Files.exists(Paths.get(documentName))) {
      println(s"Now parsing document $displayName")
      resultUrlStringList ++= parse(documentName)
      println(s"[SUCCESS] Document $displayName has been parsed!")
    } else {
      println(s"[WARNING] $displayName does not exist.")
    }

    for (i <- 1 to 50) {
      val displayName =
        s"view-source_https___exhentai.org_favorites.php_page=$i.html"
      val documentName = "/Users/christophorus/Downloads/php/" + displayName
      if (Files.exists(Paths.get(documentName))) {
        println(s"Now parsing document $displayName")
        resultUrlStringList ++= parse(documentName)
        println(s"[SUCCESS] Document $displayName has been parsed!")
      } else {
        println(s"[WARNING] $displayName does not exist.")
      }
    }

    urlPrintWriter.write(resultUrlStringList.mkString(" "))
    urlPrintWriter.close
  }

  val parse = (documentName: String) => {
    val pattern = raw"https://exhentai.org/g/[0-9]+/[0-9a-z]{10}/".r
    val bufferSource = Source.fromFile(documentName)
    val fileString = bufferSource.getLines().mkString
    bufferSource.close
    pattern.findAllMatchIn(fileString).map(_.toString)
    // for {
    //   (url, count) <- urlList.zipWithIndex if count % 2 == 0
    // } yield url
  }
}
