package hw_1_1;
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.TextOutputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class SQLCount
{
	public static class Map2 extends Mapper<LongWritable, Text, Text, Text>
	{				
		public void map(LongWritable key, Text value, Context context)
		  throws IOException, InterruptedException
		  {
			String line=value.toString(); 
			if (line.length()!=0)	
			{		
				String[] line_code = line.split("\t");				
				context.write(new Text(line_code[0]), new Text(line_code[1]));								
			}			
		  }
	}		
	public static class Map1 extends Mapper<LongWritable, Text, Text, Text>
	{
		private final static String one = "1";		
		public void map(LongWritable key, Text value, Context context)
		  throws IOException, InterruptedException
		  {
			String line=value.toString(); 
			if (line.length()!=0)	
			{		
				String[] line_cc = line.split("\t");				
				int line_pop = Integer.parseInt(line_cc[4]);
				if (line_pop > 1000000) 
				{
					context.write(new Text(line_cc[2]),new Text("1"));				
				}
			}			
		  }
	}
	
	
	public static class Reduce extends Reducer<Text,Text,Text,Text>
	{
		//private IntWritable result = new IntWritable(); <Text,Text,Text,IntWritable>
		String key_1 = "";
		String merge_1 = "";
		int merge = 0;
		Text valEmit = new Text();
	    public void reduce(Text key, Iterable<Text> values_r, Context context) 
	    		throws IOException, InterruptedException 
	    {int sum = 0;
	      int counter = 0;
	      for (Text val : values_r) 
	      {
	    	if (counter == 0) 
	    	{
	    		key_1 = val.toString();
	    	}
	    	else if (counter > 0)
	    	{   		
	    		sum += Integer .parseInt(val.toString());
	    	}
	    	
	      }	      
	      if (sum >=3)
	      {
	    	  context.write(new Text(key_1), new Text(Integer.toString(sum)));
	      }
	    }
	
	}


public static void main(String[] args) throws Exception 
{
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "SQLCount");
    
    job.setJarByClass(SQLCount.class);    
    job.setCombinerClass(Reduce.class);
    job.setReducerClass(Reduce.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);    
    //job.setInputFormatClass(TextInputFormat.class);
    //job.setOutputFormatClass(TextOutputFormat.class);
    
    //String[] files=new GenericOptionsParser(conf,args).getRemainingArgs();
	
    //Path p1=new Path(files[1]);
	//Path p2=new Path(files[2]);
	//Path p3=new Path(files[3]);
	
	MultipleInputs.addInputPath(job, new Path(args[2]), TextInputFormat.class, Map2.class);
	MultipleInputs.addInputPath(job, new Path(args[1]), TextInputFormat.class, Map1.class);
    Path outputPath = new Path(args[3]);
    
    //FileInputFormat.addInputPath(job, new Path(args[1]));
    FileOutputFormat.setOutputPath(job, outputPath);    
    /*
    for (int i = 0; i < otherArgs.length - 1; ++i) {
      FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
    }
    FileOutputFormat.setOutputPath(job,
      new Path(otherArgs[otherArgs.length - 1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
    */
    outputPath.getFileSystem(conf).delete(outputPath, true);
    System.exit(job.waitForCompletion(true) ? 0 : 1);
}

}