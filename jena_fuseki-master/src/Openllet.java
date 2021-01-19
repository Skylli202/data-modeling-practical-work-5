package openllet;

import java.io.IOException;

import java.io.IOException;
import java.nio.file.Files;

//import openllet.jena.PelletReasonerFactory;
import org.apache.jena.fuseki.main.FusekiServer;
import org.apache.jena.query.Dataset;
import org.apache.jena.rdf.model.InfModel;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.reasoner.Reasoner;
import org.apache.jena.tdb.TDBFactory;
import org.apache.jena.reasoner.ReasonerRegistry;
import org.semanticweb.owlapi.model.OWLOntologyCreationException;
import org.semanticweb.owlapi.model.OWLOntologyStorageException;

public class Openllet {
    /**
     * @param args the command line arguments
     * @throws org.semanticweb.owlapi.model.OWLOntologyCreationException
     * @throws org.semanticweb.owlapi.model.OWLOntologyStorageException
     */
    //public static void main(String[] args) {
    public static void main(String[] args) throws OWLOntologyCreationException, OWLOntologyStorageException, IOException, Exception {

        System.out.println("Jena/Fuseki OWL2 server with Openlett reasonning engine ");
        System.out.println("Jena Fuseki module documentation : https://jena.apache.org/documentation/javadoc/fuseki2-main/org/apache/jena/fuseki/main/FusekiServer.html");
        System.out.println("Openllet reasoner: https://github.com/Galigator/openllet");
        System.out.println("Jena TDB module documentation : https://jena.apache.org/documentation/javadoc/tdb/org/apache/jena/tdb/TDBFactory.html");


        String file = "";
        String config = "";
        String directory = "";
        file = "./server.owl";
        directory = "./tdb" ;
        config = "./config.ttl";

        // check whether a location already has a TDB database or whether a call to TDBFactory will cause a new, fresh TDB database to be created
        if (!TDBFactory.inUseLocation(directory)){
            // create or connect to a TDB-backed dataset
            Dataset dataset = TDBFactory.createDataset(directory);
            // create a reasoner from openllet.jena.PelletReasonerFactory
            //final Reasoner reasoner = PelletReasonerFactory.theInstance().create();
            final Reasoner reasoner = ReasonerRegistry.getRDFSReasoner();
            // create a model (empty object)
            final Model emptyModel = ModelFactory.createDefaultModel();
            // create a inference model from the reasoner and empty model
            final InfModel model = ModelFactory.createInfModel(reasoner, emptyModel);
            // read the ontology file within the inference model
            model.read(file);
            // add the model into the dataset
            dataset.getDefaultModel().add(model);
            // create fuseki server from the dataset
            FusekiServer server = FusekiServer.create()
                    .add("/ds", dataset)
                    .build();


            // start and the server for testing
            server.start();
            server.stop();
        }

        FusekiServer server = FusekiServer.create().parseConfigFile(config).
                build();

        server.start();
    }

}
