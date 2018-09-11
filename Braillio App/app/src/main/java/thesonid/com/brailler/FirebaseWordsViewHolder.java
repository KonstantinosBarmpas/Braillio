package thesonid.com.brailler;

/**
 * Created by Konstantinos Barmpas.
 */

import android.content.Context;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.TextView;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import java.util.Vector;

public class FirebaseWordsViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

    //Declare Activity variables.
    View mView;
    static Vector<String> v;
    private String[] s;
    Context mContext;
    private static String iD;
    private static DatabaseReference mReference;

    /*
        This class populates the recycler viewer with firebase data.
    */

    public FirebaseWordsViewHolder(View itemView) {
        super(itemView);
        mView = itemView;
        mContext = itemView.getContext();
        itemView.setOnClickListener(this);
    }

    /*This function creates a vector with the data so we can easily
      access the position of the adapter when the user clicks on an item.
    */
    static public void createVector() {
        v = new Vector<String>();
    }

    /*This function gets the database reference so we can update the firebase when
      on click.
    */
    static public void getRef(String id) {
        final FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference zonesRef = database.getInstance().getReference("Boards");
        DatabaseReference zone1Ref = zonesRef.child(id);
        mReference = zone1Ref.child("words");
        iD = id;
    }

    //Sets the data to the layout - recycler viewer items
    public void bindData(final String data) {
        TextView action = (TextView) mView.findViewById(R.id.word_display_recycler);
        action.setText(data);
        v.add(data);
    }

    //Gets the position on the clicked item, deletes it from the database and
    //refreshes the recycler viewer.
    @Override
    public void onClick(final View view) {
        s = v.toArray(new String[v.size()]);
        String key = s[getAdapterPosition()];
        mReference.child(key).removeValue();
        v.remove(key);
        WordActivity.setUpFirebaseAdapter(iD);
    }

}